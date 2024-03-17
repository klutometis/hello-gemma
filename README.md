# Hello, Gemma!

Have a phone-conversation with
[Gemma](https://blog.google/technology/developers/gemma-open-models/) and
[Gemini](https://gemini.google.com/) over Twilio where they play nurse-triage;
and attempt to answer questions like:

- Whom should I see about headaches?
- What about selling NVDA?
- Programmer’s block?

https://github.com/klutometis/hello-gemma/assets/85991/18505109-0db0-474f-a708-5445d0e9ed84

## Design

See [`main.py`](main.py) for the implementation; in a nutshell, though:

1. Twilio picks up the phone and does speech-to-text; then
2. Calls Gemma to classify symptoms → specialist; then
3. Gemini takes over for final answer; and finally
4. Twilio calls Google speech-to-text.
