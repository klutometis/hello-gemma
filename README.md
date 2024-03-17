# Hello, Gemma!

Have a phone-conversation with
[Gemma](https://blog.google/technology/developers/gemma-open-models/) and
[Gemini](https://gemini.google.com/) over Twilio where they play nurse-triage;
and attempt to answer questions like:

- Whom should I see about headaches?
- What about selling NVDA?
- Programmer’s block?

https://github.com/klutometis/hello-gemma/assets/85991/18505109-0db0-474f-a708-5445d0e9ed84

## Motivation

I wanted to show how baby models like Gemma (at 2B parameters) could be used for
things like cheap classification tasks without resorting to big guns like
Gemini; after these small, discrete subproblems are solved with baby models;
it's time for Gemini to step in for the final response with the appropriate
bedside-manner, etc.

Baby models and big models collaborate on problems; which preserves the
attention span of the big models for interesting problems; and also keeps costs
down, since the big models can be relied on exclusively for communication from
and to the outside world.

## Design

See [`main.py`](main.py) for the implementation; in a nutshell, though:

1. Twilio picks up the phone and does speech-to-text; then
2. Calls Gemma to classify symptoms → specialist; then
3. Gemini takes over for final answer; and finally
4. Twilio calls Google speech-to-text.
