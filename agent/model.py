"""The MODEL — the one place the agent talks to an LLM.

This is the whole point of the lab: an agent is a *wrapper around a model*.
Everything else — memory, tools, the loop — is ordinary code you can read in
agent/. This file is the only part that calls the model. Comment out the call
and the "agent" is just a Python loop with nothing to think for it.

We use a FREE model here (gpt-oss on Groq) so the lab costs nothing and runs very
fast. Groq speaks the OpenAI API, so the call and the tool-calling format are the
familiar OpenAI ones; swapping to any other OpenAI-compatible provider is a
three-line change (base URL + model + key).
"""

from __future__ import annotations

import os
import time

from openai import APIStatusError, OpenAI, RateLimitError

# An agent is a wrapper around THIS. Any OpenAI-compatible provider works — just
# change these three lines and set the matching key:
#   Groq (free, very fast) -> this default. Current free models: console.groq.com/docs/models
#       https://api.groq.com/openai/v1  ·  openai/gpt-oss-120b  ·  GROQ_API_KEY
#   Google Gemini (free, no card)
#       https://generativelanguage.googleapis.com/v1beta/openai/  ·  gemini-3.8-flash  ·  GEMINI_API_KEY
#   OpenAI, or a local Ollama -> same pattern.
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "openai/gpt-oss-120b"       # free + fast + reliable tool calling
API_KEY_ENV = "GROQ_API_KEY"

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        # Get a free key at https://console.groq.com (sign in, "API Keys").
        _client = OpenAI(base_url=BASE_URL, api_key=os.environ.get(API_KEY_ENV))
    return _client


def call_model(messages: list[dict], tools: list[dict], max_retries: int = 4):
    """One round-trip to the model. Returns the model's raw reply.

    The reply is either final text, or a request to call one or more tools (then
    ``reply.choices[0].message.tool_calls`` is populated). We don't interpret it
    here — that's the harness's job. This function just passes the conversation
    so far and the available ``tools`` to the model and hands back the reply.

    The free tier is shared, so a busy moment can return 429 (rate limited) or a
    brief 5xx. We wait and retry a few times with exponential backoff rather than
    crash. If it still fails, the error is raised so you can see what happened.
    """
    client = _get_client()
    # Omit `tools` entirely when there are none — sending an empty list makes some
    # models return nothing. No tools offered => the model must answer in text.
    kwargs = {"model": MODEL, "max_tokens": 1024, "messages": messages}
    if tools:
        kwargs["tools"] = tools
    delay = 2.0
    for attempt in range(max_retries + 1):
        try:
            return client.chat.completions.create(**kwargs)
        except (RateLimitError, APIStatusError) as exc:
            retryable = isinstance(exc, RateLimitError) or getattr(exc, "status_code", 0) >= 500
            if not retryable or attempt == max_retries:
                raise
            print(f"[model busy: {type(exc).__name__}; retrying in {delay:.0f}s]")
            time.sleep(delay)
            delay *= 2
