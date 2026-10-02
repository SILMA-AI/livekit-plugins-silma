#!/usr/bin/env python3
"""A voice agent using the SILMA TTS plugin: Deepgram STT -> OpenAI LLM -> SILMA TTS.

Setup:

    pip install livekit-plugins-silma "livekit-agents[silero,deepgram,openai]>=1.8.0" python-dotenv

    export SILMA_API_KEY="..."
    export DEEPGRAM_API_KEY="..."
    export OPENAI_API_KEY="..."

Talk to it in your terminal with your own microphone (no LiveKit server needed):

    python agent.py download-files   # once: fetches the VAD and turn-detector models
    python agent.py console

Or connect it to a LiveKit server and talk to it from https://agents-playground.livekit.io:

    export LIVEKIT_URL="wss://..." LIVEKIT_API_KEY="..." LIVEKIT_API_SECRET="..."
    python agent.py dev

Set LANGUAGE=en to use the English model.
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

from livekit.agents import Agent, AgentServer, AgentSession, JobContext, cli
from livekit.plugins import deepgram, openai, silero, silma

load_dotenv()

logging.getLogger("livekit.plugins.silma").setLevel(logging.DEBUG)

LANGUAGE = os.getenv("LANGUAGE", "ar")
if LANGUAGE.startswith("en"):
    MODEL, VOICE = "silma-tts-v2-english", "emma"
    INSTRUCTIONS = "You are a friendly voice assistant. Speak English."
    GREETING = "Hello! I'm your voice assistant. You can reach us on <STAG_PN>92005455</STAG_PN>."
else:
    MODEL, VOICE = "silma-tts-v2-msa", "maryam"
    INSTRUCTIONS = "You are a friendly voice assistant speaking Modern Standard Arabic."
    GREETING = "مرحبا بك! أنا مساعدك الصوتي. للتواصل معنا اتصل على <STAG_PN>92005455</STAG_PN>."

INSTRUCTIONS += (
    " Keep replies to one or two short sentences, because they are spoken aloud."
)

server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext) -> None:
    session = AgentSession(
        # Arabic requires nova-3, and `filler_words` is English-only at Deepgram.
        stt=deepgram.STT(model="nova-3", language=LANGUAGE, filler_words=LANGUAGE.startswith("en")),
        llm=openai.LLM(model="gpt-6-luna"),
        tts=silma.TTS(model=MODEL, voice=VOICE),
        vad=silero.VAD.load(),
    )

    await session.start(agent=Agent(instructions=INSTRUCTIONS), room=ctx.room)
    await session.say(GREETING)


if __name__ == "__main__":
    print(f"livekit-plugins-silma {silma.__version__} from {silma.__file__}")
    cli.run_app(server)
