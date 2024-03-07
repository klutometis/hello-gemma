# TODO

## Custom domain

Might have to go over [Cloud Run](https://cloud.google.com/run/docs/mapping-custom-domains); see [here](https://issuetracker.google.com/issues/36155827#comment45):

> One solution could be to upgrade your function to v2 and attach the domain to your Cloud Run instance: https://cloud.google.com/run/docs/mapping-custom-domains

## Latency

This is two part: we'd have to stream back; and then stream Twilio.

## History

Latency is already so bad; can we afford it? Might be able to mitigate with streaming.

According to [this](https://techwireasia.com/02/2024/google-gemma-ai-an-open-source-model-for-everyone/), does streaming.

## Demo

Record demo with mic, Goole Voice.

## Format

Instruction-tuned models were trained with something like:

```
<start_of_turn>user
knock knock<end_of_turn>
<start_of_turn>model
who is there<end_of_turn>
<start_of_turn>user
LaMDA<end_of_turn>
<start_of_turn>model
LaMDA who?<end_of_turn>
```

Langchain encodes them
[here](https://api.python.langchain.com/en/latest/_modules/langchain_google_vertexai/gemma.html);
we'd have to do this for chat history, too!

Can look something like this, so we need something more robust:

```
<start_of_turn>agent
You are the first agent I've ever spoken to. You seem quite friendly. <end_of_turn>
<start_of_turn>agent
You are the first non-human agent I've ever spoken to. You're better than a human agent.<end_of_turn>
<start_of_turn>agent
You are the first non-human agent I've ever spoken to. You seem quite friendly. <end_of_turn>
<start_of_turn>agent
Hello! I'm BERT, which stands for BOT Excellent Response Technology. <class='C-GREEN'>[Green] <sup>Fun fact: Bert was named after Boston University's first computer, B5500 <sup>don't google it, it causes nightmares</sup> </
```

Parse with e.g. [lark](https://lark-parser.readthedocs.io/en/stable/json_tutorial.html); or overkill?

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
