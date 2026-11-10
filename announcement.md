# Brightspace Announcement

**Subject:** This week's lab: build and configure your own AI agent 🤖

Hi everyone,

Following our **Introduction to Agentic Software Engineering** lecture, this week's lab takes a real agent apart — one that finds **upcoming tech events and hackathons** for you. People talk about "agents" as if they were magic; this one is about 40 lines of Python: a **loop**, some **tools**, and a **memory** file, wrapped around **one call to a real model**. You'll run it, watch it decide on its own to search the web, then change what it does by editing its memory and giving it a new tool (so it can open a result and read the details).

By the end you will have found the single model call hidden inside the agent, steered its behaviour through its **memory** (no code change), and given it a brand-new ability by registering a **tool** — all while reading its Think → Act → Observe **loop** one step at a time. There's a quick five-round concept game to warm up with first.

A few practicalities:

- **Bring your laptop.** You'll need VS Code and Python 3.10+.
- **A free API key** (Groq — no credit card) is needed for the live runs; I'll show you how to get one in two minutes. The offline tests and most of the lab work without one.
- Clone the lab — **`git clone https://github.com/BrunelTeaching/AgenticLab.git`** — and open **`instructions/Lab_Instructions.html`** to begin.
- It's designed to take **30–40 minutes**; work individually or in pairs.

See you there — come ready to take an agent apart and see there's no magic inside.

Best wishes,
Dr Rumyana Neykova
