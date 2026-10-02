# SILMA AI plugin for LiveKit Agents

Support for English and Arabic speech synthesis with [SILMA AI](https://silma.ai/)
TTS v2 — Modern Standard Arabic, the Saudi (Najdi) dialect, and English.

This plugin is maintained by SILMA AI and published independently of the
[LiveKit Agents](https://github.com/livekit/agents) repository.

## Installation

```bash
pip install livekit-plugins-silma
```

Requires `livekit-agents>=1.8`.

## Pre-requisites

You'll need an API key from [SILMA](https://app.silma.ai/api-keys). Set it as an
environment variable:

```bash
export SILMA_API_KEY="..."
```

## Usage

```python
from livekit.agents import AgentSession
from livekit.plugins import silma

session = AgentSession(
    tts=silma.TTS(
        model="silma-tts-v2-msa",
        voice="sarah",
    ),
    # ... stt, llm, vad
)
```

### Models and voices

| Model | Language | Voices |
| --- | --- | --- |
| `silma-tts-v2-english` | English | `james`, `emma` |
| `silma-tts-v2-msa` | Modern Standard Arabic | `sarah`, `salma`, `salwa`, `saja`, `sultan`, `salman`, `sulaiman`, `salim` |
| `silma-tts-v2-ksa` | Arabic, Saudi (Najdi) dialect | same as MSA |

### Cloned voices

Upload a voice under **Custom Voices** at https://app.silma.ai/voices and pass
its id along with your user id:

```python
silma.TTS(
    model="silma-tts-v2-ksa",
    voice="sarah",
    user_id="...",
    custom_audio_id="voice_1769817467123",
)
```

### Pronunciation hints

SILMA reads phone numbers, emails and links correctly when they are tagged in
the text:

```python
await session.say(
    "You can reach us on <STAG_PN>92005455</STAG_PN> or at <STAG_EMAIL>hi@silma.ai</STAG_EMAIL>."
)
```

The plugin keeps these tags intact when it splits text, so a tag is never cut in
half across two requests.

Account-level pronunciation overrides configured at https://app.silma.ai/control
are applied when you pass `user_id` and
`enable_server_pronunciation_overrides=True`.

## How it works

`stream()` uses the realtime WebSocket API (`wss://api.silma.ai/tts/v2/ws/stream`)
and sentence-tokenizes incoming LLM text so each request is a complete
utterance. `synthesize()` uses the binary streaming endpoint
(`POST /stream`).

SILMA caps `text` at 250 characters per request, so longer input is split on
word boundaries and sent as sequential requests concatenated into one audio
segment.

SILMA returns a 24 kHz mono float32 waveform; the plugin converts it to 16-bit
PCM for the agent pipeline.


## Development

```bash
pip install -e ".[dev]"
pytest
```

### Releasing

1. Bump `__version__` in `livekit/plugins/silma/version.py` and add a
   `CHANGELOG.md` entry.
2. Commit, then tag and push: `git tag v0.1.0 && git push origin v0.1.0`.
3. The `Publish` workflow builds the package and uploads it to PyPI via
   trusted publishing.

## License

Apache-2.0
