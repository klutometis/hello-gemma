import functools
import json
import logging
from enum import Enum
from http import HTTPStatus

import functions_framework
from langchain.output_parsers.enum import EnumOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_google_vertexai import GemmaChatVertexAIModelGarden
from pyparsing import Literal, SkipTo, StringEnd
from twilio.twiml.voice_response import Gather, Say, VoiceResponse


@functools.lru_cache(maxsize=None)
def get_model() -> GemmaChatVertexAIModelGarden:
    return GemmaChatVertexAIModelGarden(
        project=get_param("project"),
        location=get_param("location"),
        endpoint_id=get_param("endpoint"),
        parse_response=True,
    )


def get_param(key: str) -> str:
    with open("params.json", "r") as file:
        return json.load(file)[key]


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


def generate(prompt):
    class Specialties(Enum):
        INTERNAL_MEDICINE = "Internal Medicine"
        PEDIATRICS = "Pediatrics"
        ORTHOPEDICS = "Orthopedics"
        CARDIOLOGY = "Cardiology"
        NEUROLOGY = "Neurology"

    parser = EnumOutputParser(enum=Specialties)

    conversation = ChatPromptTemplate.from_messages(
        [
            HumanMessagePromptTemplate.from_template(
                "You're a nurse whose job is to triage patients into one"
                " of the specialties. {instructions}"
            ),
            AIMessage("Ok!"),
            HumanMessage("My tummy hurts", example=True),
            AIMessage("Internal Medicine", example=True),
            HumanMessagePromptTemplate.from_template("{prompt}"),
        ]
    ).partial(instructions=parser.get_format_instructions())

    chain = (
        {"prompt": RunnablePassthrough()}
        | conversation
        | get_model()
        | parse_gemma
        | parser
    )

    return chain.invoke(prompt).value


# NB(danenberg): Cloud functions are stateless; so the docs recommend
# a lazy-initialized global for capturing expensive things like
# models, etc.*
#
# In this case, we'll prime the memoization at cold-start.
#
# * https://cloud.google.com/functions/docs/bestpractices/tips#use_global_variables_to_reuse_objects_in_future_invocations # noqa: 501
model = get_model()


@functions_framework.http
def hello(request):
    GREETING = "Hi, I'm Gemma! How can I help you today?"
    HEADERS = {"Content-Type": "text/xml"}

    logging.info(request.form.to_dict())

    speech_result = request.form.get("SpeechResult")

    suffix = None

    if speech_result:
        suffix = generate(speech_result)

    logging.info(suffix)

    response = VoiceResponse()
    gather = Gather(
        input="speech",
        enhanced="true",
        speech_model="phone_call",
        barge_in=True,
    )
    gather.append(say(suffix if suffix else GREETING))
    response.append(gather)
    response.append(say("Thanks for calling!"))

    return response.to_xml(), HTTPStatus.OK, HEADERS
