# TODO

## Gemma

See Gemma on [Hugging Face](https://huggingface.co/google/gemma-7b) and
[Vertex AI](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/335;publisherModelVersion=gemma-7b-gg-hf).

## Nested

See e.g.:

```Python
from twilio.twiml.voice_response import Gather, VoiceResponse, Say

response = VoiceResponse()
gather = Gather(input='speech dtmf', timeout=3, num_digits=1)
gather.say('Please press 1 or say sales for sales.')
response.append(gather)

print(response)
```

## Stopping condition

See e.g.
[`actionOnEmptyResult](https://www.twilio.com/docs/voice/twiml/gather#actiononemptyresult):

> actionOnEmptyResult allows you to force <Gather> to send a webhook to the
> action url even when there is no DTMF input. By default, if <Gather> times out
> while waiting for DTMF input, it will continue on to the next TwiML
> instruction.

I want to know whether we can distinguish these cases:

- Initial call
- Empty input
- Non-empty input

Might be able to avoid the multiple endpoints, since we're using cloud
functions.

## Models

Might try
[different models](https://www.twilio.com/docs/voice/twiml/gather#speechmodel)
such as: `experimental_conversations`, `phone_call`? Also see
[enhanced](https://www.twilio.com/docs/voice/twiml/gather#speechmodel).

## Partial callbakcs

[Unstable results](https://demo.twilio.com/docs/classic.mp3) are interesting;
gather in a quasi-stream?

## Websockets

See
[bidirectional streaming in Twilio](https://stackoverflow.com/questions/75475925/stream-audio-back-to-twilio-via-websocket-connection);
as well as
[Elevenlabs websockets](https://elevenlabs.io/docs/api-reference/websockets).

In
[reducing latency](https://elevenlabs.io/docs/api-reference/reducing-latency),
mentions [streaming](https://elevenlabs.io/docs/api-reference/streaming); which
streams audio as it's being generated.

## Local development

See https://cloud.google.com/functions/docs/running/function-frameworks

## Deployment

- https://cloud.google.com/build/docs/deploying-builds/deploy-functions#configuring_the_deployment
- https://cloud.google.com/build/docs/deploying-builds/deploy-functions#continuous_deployment

I see the weird YAML / JSON thing from
[this article](https://faun.pub/google-appengine-bazel-how-to-deploy-to-appengine-flexible-using-bazel-and-google-cloud-deploy-469c0c64bc35).

Can similarly
[build and push a container](https://github.com/GoogleCloudPlatform/cloud-builders/blob/master/bazel/README.md#build-and-push-a-container-image).

## Cloud functions

See:

- https://cloud.google.com/functions/docs/running/function-frameworks
- https://cloud.google.com/functions/docs/create-deploy-gcloud

Also
[C++ in Lambda](https://www.reddit.com/r/cpp/comments/a1jo6r/c_now_supported_in_aws_lambda/).

## Twilio

- https://www.twilio.com/docs/voice/tutorials/build-interactive-voice-response-ivr-phone-tree/python
- https://www.twilio.com/en-us/blog/test-your-webhooks-locally-with-ngrok-html
- https://www.twilio.com/docs/voice/sdks

[Programmable voice](https://www.twilio.com/docs/voice/sdks) is the thing,
though.

## Cloud Run vs. Cloud Function

This guy did
[bash in Cloud Run](https://medium.com/google-cloud/executing-bash-scripts-with-a-webhook-in-google-cloud-75ea4b173c9);
similarly C++?
