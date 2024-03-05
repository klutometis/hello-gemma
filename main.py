import functions_framework
import json
import logging
import re

from twilio.twiml.voice_response import VoiceResponse, Gather, Say
from http import HTTPStatus
from google.cloud import aiplatform


def get_param(key: str) -> str:
    with open("params.json", "r") as file:
        return json.load(file)[key]


def say(text):
    return Say(text, voice="Google.en-US-Neural2-H")


def generate(prompt):
    PROMPT = """<start_of_turn>user
You're Gemma, a helpful agent on the phone; please keep responses short and relevant!<end_of_turn>
<start_of_turn>model
Ok!<end_of_turn>
<start_of_turn>user
{prompt}<end_of_turn>"""

    # Initialize the Vertex AI client
    client_options = {
        "api_endpoint": f"{get_param('location')}-aiplatform.googleapis.com"
    }
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # Construct the full path of the endpoint
    endpoint = client.endpoint_path(
        project=get_param("project"),
        location=get_param("location"),
        endpoint=get_param("endpoint"),
    )

    # Prepare your input for the model
    instances = [
        {
            "inputs": PROMPT.format(prompt=prompt),
            "parameters": {
                "max_new_tokens": 50,
                "temperature": 1.0,
                "top_p": 1.0,
                "top_k": 1.0,
            },
        },
    ]
    # Make the prediction request
    response = client.predict(endpoint=endpoint, instances=instances)

    logging.error(response)

    if not response.predictions:
        return None

    prediction = response.predictions[0]

    logging.error(prediction)

    # TODO(danenberg): Should be able to do better than this: will truncate anything with `<`.
    pattern = r"\n<start_of_turn>model\n([^<]*)"

    match = re.search(pattern, prediction, re.DOTALL)

    logging.error(match)

    if match:
        return match.group(1)  # Group 1 is the first capturing group (.*?)

    return None


@functions_framework.http
def hello(request):
    GREETING = "Hi, I'm Gemma! How can I help you today?"
    HEADERS = {"Content-Type": "text/xml"}

    logging.error(request.form.to_dict())

    speech_result = request.form.get("SpeechResult")

    suffix = None

    if speech_result:
        suffix = generate(speech_result)

    logging.error(suffix)

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
