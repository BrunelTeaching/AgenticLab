#!/usr/bin/env bash
# Run the baseline (offline) test suite. No API key needed for the tests.
set -u
echo "==================== pytest (offline baseline) =============="
pytest -q
echo
echo "To run the agent for real, set your FREE key and ask a question:"
echo '  export GROQ_API_KEY=gsk_...        # use the class key, or get one at https://console.groq.com'
echo '  python run.py "AI hackathons for students in London this term"'
