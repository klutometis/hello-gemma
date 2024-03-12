# TODO

## 2b

See [formatting](https://ai.google.dev/gemma/docs/formatting).

```json
{
  "instances": [
    {
      "prompt": "<start_of_turn>user\nYou're a nurse whose job is to triage patients into one of the specialties: Internal Medicine, Pediatrics, Orthopedics, Cardiology, Neurology. Answer with the specialty only.<end_of_turn>\n<start_of_turn>model\nok</end_of_turn>\n<start_of_turn>user\nMy tummy hurts <end_of_turn>\n<start_of_turn>model\nInternal Medicine<end_of_turn>\n<start_of_turn>user\nMy heart aches<end_of_turn>\n<start_of_turn>model"
    }
  ]
}
```

Gets:

```json
{
  "predictions": [
    "Prompt:\n<start_of_turn>user\nYou're a nurse whose job is to triage patients into one of the specialties: Internal Medicine, Pediatrics, Orthopedics, Cardiology, Neurology. Answer with the specialty only.<end_of_turn>\n<start_of_turn>model\nok</end_of_turn>\n<start_of_turn>user\nMy tummy hurts <end_of_turn>\n<start_of_turn>model\nInternal Medicine<end_of_turn>\n<start_of_turn>user\nMy heart aches<end_of_turn>\n<start_of_turn>model\nOutput:\nCardiology<end_of_turn>\n<start_of_"
  ]
}
```

And see if the 7b can do a reasonable job at final response synthesis. Just
naïve regex; failing that, truncate response.

7b:

```json
{
  "instances": [
    {
      "prompt": "<start_of_turn>user\nYou're a hospital receptionist whose job is to guide patients with certain symtoms to a specialist. Can you guide them with a flawless bedside manner?<end_of_turn>\n<start_of_turn>model\nok</end_of_turn>\n<start_of_turn>user\nSymptoms: My tummy hurts\nSpecialist: Internal Medicine<end_of_turn>\n<start_of_turn>model\nI hear your tummy aches! Sorry to hear that. Let me get you to internal medicine.<end_of_turn>\n<start_of_turn>user\nSymptoms: My heart aches\nSpecialty: Cardiology<end_of_turn>\n<start_of_turn>model"
    }
  ]
}
```

gets:

```json
{
  "predictions": [
    "Prompt:\n<start_of_turn>user\nYou're a hospital receptionist whose job is to guide patients with certain symtoms to a specialist. Can you guide them with a flawless bedside manner?<end_of_turn>\n<start_of_turn>model\nok</end_of_turn>\n<start_of_turn>user\nSymptoms: My tummy hurts\nSpecialist: Internal Medicine<end_of_turn>\n<start_of_turn>model\nI hear your tummy aches! Sorry to hear that. Let me get you to internal medicine.<end_of_turn>\n<start_of_turn>user\nSymptoms: My heart aches\nSpecialty: Cardiology<end_of_turn>\n<start_of_turn>model\nOutput:\nYour heart feels lousy, huh? You'd probably benefit from seeing a"
  ]
}
```

## Demo

2b for triage; 7b for constrained final answer; see if we can tune. Both in
Discord.

## Finetuning

See
[finetuning on Vertex](https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/community/model_garden/model_garden_gemma_finetuning_on_vertex.ipynb).

## Custom domain

Might have to go over
[Cloud Run](https://cloud.google.com/run/docs/mapping-custom-domains); see
[here](https://issuetracker.google.com/issues/36155827#comment45):

> One solution could be to upgrade your function to v2 and attach the domain to
> your Cloud Run instance:
> https://cloud.google.com/run/docs/mapping-custom-domains

[Cloudflare / cloudfront](https://stackoverflow.com/questions/71815143/how-can-i-call-my-aws-lambda-function-url-via-a-custom-domain)
with AWS Lambda; also,
[deploy to Cloud Run](https://github.com/google-github-actions/deploy-cloudrun?tab=readme-ov-file#authorization)
with GitHub action; see also
[serverless AWS](https://aws.amazon.com/serverless/); GitHub
[deploy to Fargate](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-amazon-elastic-container-service);
[deploy to GKE](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-google-kubernetes-engine).

## Streaming

See
[streaming Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/streaming);
which uses this
[`TextGenerationModel`](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/streaming#sdk)
abstraction, though: can `TextGenerationModel` be used with arbitrary endpoints?

Can
[`from_pretrained`](https://cloud.google.com/python/docs/reference/aiplatform/latest/vertexai.language_models.TextGenerationModel#vertexai_language_models_TextGenerationModel_from_pretrained)
be used with our endpoint?

Oh,
[this](https://github.com/google-deepmind/dramatron/blob/58339443e7fbaec21fe5f5e246266f1e8b1d7ee4/colab/dramatron.ipynb#L2396)
is interesting:

```Python
    if 'bison' in self._model:
      self._client = TextGenerationModel.from_pretrained(model)
    elif 'gemini' in self._model:
      self._client = genai.GenerativeModel(model)
```

Wait, PHP has
[`streamingPredict`](https://cloud.google.com/php/docs/reference/cloud-ai-platform/latest/V1.Client.PredictionServiceClient#_Google_Cloud_AIPlatform_V1_Client_PredictionServiceClient__streamingPredict__);
what about Python?

Hilarious: Python only has
[`predict`](https://cloud.google.com/python/docs/reference/automl/latest/google.cloud.automl_v1beta1.services.prediction_service.PredictionServiceClient#google_cloud_automl_v1beta1_services_prediction_service_PredictionServiceClient_predict);
doesn't stream?

[`streaming_predict`](https://github.com/googleapis/python-aiplatform/blob/f294ba8b762a88b77a623b86145302c976fdabc4/google/cloud/aiplatform_v1/services/prediction_service/client.py#L1561)
is in the code but undocumented?

There's also
[`generate_content`](https://github.com/googleapis/python-aiplatform/blob/f294ba8b762a88b77a623b86145302c976fdabc4/google/cloud/aiplatform_v1/services/prediction_service/client.py#L2002)
and
[`stream_generate_content`](https://github.com/googleapis/python-aiplatform/blob/f294ba8b762a88b77a623b86145302c976fdabc4/google/cloud/aiplatform_v1/services/prediction_service/client.py#L2127);
which are higher level: uses
[`GenerateContentRequest`](https://github.com/googleapis/googleapis/blob/792dacbd24643d8650fbf705b3f745532012ea34/google/ai/generativelanguage/v1/generative_service.proto#L111)
and
[`Content`](https://github.com/googleapis/googleapis/blob/792dacbd24643d8650fbf705b3f745532012ea34/google/cloud/aiplatform/v1/content.proto#L55 "https://github.com/googleapis/googleapis/blob/792dacbd24643d8650fbf705b3f745532012ea34/google/cloud/aiplatform/v1/content.proto#L55")
with roles.

The
[`GenerateContentResponse`](https://github.com/googleapis/python-aiplatform/blob/f294ba8b762a88b77a623b86145302c976fdabc4/google/cloud/aiplatform_v1/types/prediction_service.py#L796)
has
[`Candidate`](https://github.com/googleapis/python-aiplatform/blob/f294ba8b762a88b77a623b86145302c976fdabc4/google/cloud/aiplatform_v1/types/content.py#L479)
with `Content` (roles, etc.).

Saves having to parse? Or do we have to define these things for Gemma?

## Latency

This is two part: we'd have to stream back; and then stream Twilio.

## History

Latency is already so bad; can we afford it? Might be able to mitigate with
streaming.

According to
[this](https://techwireasia.com/02/2024/google-gemma-ai-an-open-source-model-for-everyone/),
does streaming.

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

Parse with e.g.
[lark](https://lark-parser.readthedocs.io/en/stable/json_tutorial.html); or
overkill?

See
[here](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/ai-services/openai/includes/chat-markup-language.md#working-with-chat-markup-language-chatml)
for Microsoft's explanation of ChatML; and
[Hacker news](https://news.ycombinator.com/item?id=34988748); is wrapped by
[chat completions](https://platform.openai.com/docs/guides/text-generation/chat-completions-api).

[Output parser](https://www.reddit.com/r/LangChain/comments/166jxzi/output_parser_for_openai_chat_models/)
404s; ah, see
[output parsers](https://python.langchain.com/docs/modules/model_io/output_parsers/).

Parser / generators embedded in the various Google / OpenAI libraries; does it
make sense to write a general library; or it's wedded to the individual models?

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
