#!/usr/bin/env python3
"""Ask the events finder what's on, and watch the loop.

    python run.py "AI hackathons for students in London this term"
    python run.py "free tech meetups near Uxbridge"
    python run.py "What is a hackathon?"      # a question it can answer with no search
    python run.py                             # uses a default request

Needs a key:  export GROQ_API_KEY=gsk_...   (use the class key, or get one free at https://console.groq.com)

Every Think -> Act -> Observe step is printed, so you can see the agent decide
whether to search before it answers. Tell it your interests and your city.
"""

import sys
from pathlib import Path

from agent import run

WORKSPACE = Path(__file__).parent / "workspace"

DEFAULT_REQUEST = "upcoming student hackathons and tech meetups near London"


def main() -> None:
    request = " ".join(sys.argv[1:]).strip() or DEFAULT_REQUEST
    print("=" * 72)
    try:
        run(request, WORKSPACE, log=print)
    except Exception as exc:  # most often a busy shared key
        print(f"\nError: {type(exc).__name__}: {exc}")
        print("If the shared key is busy, make your own free one (2 min) at "
              "https://console.groq.com and `export GROQ_API_KEY=...`, or ask in the lab.")
    print("=" * 72)


if __name__ == "__main__":
    main()
