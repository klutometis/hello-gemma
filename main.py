import functools
import json
import logging
import textwrap
from enum import Enum
from http import HTTPStatus
from types import SimpleNamespace

import functions_framework
from langchain.globals import set_debug
from langchain.output_parsers.enum import EnumOutputParser
from langchain.output_parsers.fix import OutputFixingParser
from langchain.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, SystemMessage
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_vertexai import GemmaChatVertexAIModelGarden, VertexAI
from pyparsing import Literal, SkipTo, StringEnd
from twilio.twiml.voice_response import Gather, Say, VoiceResponse


@functools.cache
def get_param(key: str) -> str:
    with open("data/params.json", "r") as file:
        return json.load(file)[key]


@functools.cache
def get_gemma() -> GemmaChatVertexAIModelGarden:
    return GemmaChatVertexAIModelGarden(
        project=get_param("project"),
        location=get_param("location"),
        endpoint_id=get_param("endpoint"),
        parse_response=True,
        temperature=0,
    )


@functools.cache
def get_gemini() -> VertexAI:
    return VertexAI(mode_name="gemini-1.0-pro")


# NB(danenberg): Cloud functions are stateless; so the docs recommend
# a lazy-initialized global for capturing expensive things like
# models, etc.*
#
# In this case, we'll prime the memoization at cold-start.
#
# * https://cloud.google.com/functions/docs/bestpractices/tips#use_global_variables_to_reuse_objects_in_future_invocations # noqa: 501
gemma = get_gemma()
gemini = get_gemini()


def say(text):
    return Say(text, voice="Google.en-US-Neural2-H")


# TODO(danenberg): Doesn't stream;* but should? Only needed for
# smallish responses from baby model for now; let's punt.
#
# * https://python.langchain.com/docs/modules/model_io/output_parsers/custom#runnable-lambdas-and-generators # noqa: 501
def parse_gemma(ai_message: AIMessage) -> str:
    grammar = Literal("Output:\n") + SkipTo(
        "<end_of_turn>" | StringEnd()
    ).setResultsName("output")

    return grammar.parseString(ai_message.content)["output"]


def find_specialist(prompt):
    global gemma

    class Specialties(Enum):
        INTERNAL_MEDICINE = "Internal Medicine"
        ORTHOPEDICS = "Orthopedics"
        CARDIOLOGY = "Cardiology"
        NEUROLOGY = "Neurology"
        PSYCHIATRY = "Psychiatry"
        HOSPICE = "Hospice"

    def log_weird_specialty_and_return_default(**kwargs):
        logging.error(f"Weird specialty: {kwargs.get('completion', '∅')}")
        return Specialties.HOSPICE.value

    specialty_parser = OutputFixingParser(
        parser=EnumOutputParser(enum=Specialties),
        retry_chain=SimpleNamespace(
            run=log_weird_specialty_and_return_default
        ),
    )

    gemma_parser = RunnableLambda(parse_gemma)

    example_prompt = ChatPromptTemplate.from_messages(
        [
            HumanMessagePromptTemplate.from_template(
                "{symptoms}", example=True
            ),
            AIMessagePromptTemplate.from_template("{specialty}", example=True),
        ]
    )

    examples = [
        {"symptoms": "My tummy hurts", "specialty": "Internal Medicine"}
    ]

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt, examples=examples
    )

    # NB(danenberg): Gemma doesn't do system prompts, only model and user.
    conversation = ChatPromptTemplate.from_messages(
        [
            HumanMessagePromptTemplate.from_template(
                "You're a nurse whose job is to triage patients into "
                "one of the specialties. {specialties}. Respond with "
                "the specialty in one or two words at most."
            ),
            AIMessage("Ok!"),
            few_shot_prompt,
            HumanMessagePromptTemplate.from_template("{prompt}"),
        ]
    ).partial(specialties=specialty_parser.get_format_instructions())

    chain = (
        {"prompt": RunnablePassthrough()}
        | conversation
        | gemma
        | gemma_parser
        | specialty_parser
    )

    return chain.invoke(prompt).value


def triage(symptoms, specialist):
    global gemini

    @functools.cache
    def nurse():
        with open("data/nurse.prompt") as nurse:
            return nurse.read()

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(nurse()),
            HumanMessagePromptTemplate.from_template(
                textwrap.dedent(
                    """\
         Here are my symptoms: {symptoms}
         Here is the specialist I'd like to see: {specialist}
         """
                )
            ),
        ]
    )

    return (prompt | gemini).invoke(
        {"symptoms": symptoms, "specialist": specialist}
    )


@functions_framework.http
def hello(request):
    GREETING = "Hi, I'm Gemma; your triage nurse! How are you feeling today?"
    HEADERS = {"Content-Type": "text/xml"}

    set_debug(True)

    logging.info(f"{request.form.to_dict()=}")

    speech_result = request.form.get("SpeechResult")

    greeting = GREETING

    if speech_result:
        specialist = find_specialist(speech_result)
        logging.info(f"{specialist=}")
        greeting = triage(speech_result, specialist)
        logging.info(f"{greeting=}")

    response = VoiceResponse()
    gather = Gather(
        input="speech",
        enhanced="true",
        speech_model="phone_call",
        barge_in=True,
    )
    gather.append(say(greeting))
    response.append(gather)
    response.append(say("Thanks for calling!"))

    return response.to_xml(), HTTPStatus.OK, HEADERS
