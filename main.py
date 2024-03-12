from http import HTTPStatus
import json
import logging
import re

import functions_framework
from google.cloud import aiplatform
from google.cloud import aiplatform_v1
from twilio.twiml.voice_response import Gather, Say, VoiceResponse


def get_param(key: str) -> str:
  with open("params.json", "r") as file:
    return json.load(file)[key]


def say(text):
  return Say(text, voice="Google.en-US-Neural2-H")


def generate(prompt):
  PROMPT = """<start_of_turn>user
You're a nurse whose job is to triage patients into one of the specialties: Internal Medicine, Pediatrics, Orthopedics, Cardiology, Neurology. Answer with the specialty only.<end_of_turn>
<start_of_turn>model
ok</end_of_turn>
<start_of_turn>user
My tummy hurts<end_of_turn>
<start_of_turn>model
Internal Medicine<end_of_turn>
<start_of_turn>user
{prompt}<end_of_turn>
<start_of_turn>model"""

  # Initialize the Vertex AI client
  client_options = {
      "api_endpoint": f"{get_param('location')}-aiplatform.googleapis.com"
  }
  client = aiplatform_v1.PredictionServiceClient(client_options=client_options)

  # Construct the full path of the endpoint
  endpoint = client.endpoint_path(
      project=get_param("project"),
      location=get_param("location"),
      endpoint=get_param("endpoint"),
  )

  # Prepare your input for the model
  instances = [{
      "prompt": PROMPT.format(prompt=prompt),
  }]

  # NB(danenberg): These parameters don't seem to have any effect.
  parameters = {
      "max_output_tokens": 256,
      "temperature": 1.0,
      "top_p": 1.0,
      "top_k": 1.0,
  }

  request = aiplatform_v1.PredictRequest(
      endpoint=endpoint, parameters=parameters
  )

  request.instances.extend(instances)

  # Make the prediction request
  response = client.predict(request=request)

  logging.error(response)

  if not response.predictions:
    return None

  prediction = response.predictions[0]

  logging.info(prediction)

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
