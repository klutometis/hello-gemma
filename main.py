import logging
import functions_framework

from twilio.twiml.voice_response import VoiceResponse, Gather, Say
from http import HTTPStatus


def say(text):
    return Say(text, voice="Google.en-US-Neural2-H")


@functions_framework.http
def hello(request):
    GREETING = "Hi, I'm Gemma! How can I help you today?"
    HEADERS = {"Content-Type": "text/xml"}

    logging.error(request.form.to_dict())

    speech_result = request.form.get("SpeechResult")

    response = VoiceResponse()
    gather = Gather(
        input="speech",
        enhanced="true",
        speech_model="phone_call",
        barge_in=True,
    )
    gather.append(say(speech_result if speech_result else GREETING))
    response.append(gather)
    response.append(say("Thanks for calling!"))

    return response.to_xml(), HTTPStatus.OK, HEADERS
