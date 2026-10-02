# Changelog

All notable changes to **livekit-plugins-silma** will be documented in this file.


## [0.1.0] - 2026-10-02

### Added

- `silma.TTS`, a LiveKit Agents TTS plugin for SILMA TTS v2, covering English
  (`silma-tts-v2-english`), Modern Standard Arabic (`silma-tts-v2-msa`) and the
  Saudi Najdi dialect (`silma-tts-v2-ksa`).

- `stream()` over SILMA's realtime WebSocket API, sentence-tokenizing incoming
  LLM text, and `synthesize()` over the binary HTTP streaming endpoint.

- Conversion of SILMA's 24 kHz float32 waveform to 16-bit PCM, buffering
  samples that straddle a chunk boundary.

- Automatic splitting of text over the API's 250-character limit, on word
  boundaries, keeping `<STAG_PN>` / `<STAG_EMAIL>` / `<STAG_LINK>` pronunciation
  hints intact across the split.

- Cloned voices via `custom_audio_id`, and account pronunciation overrides via
  `enable_server_pronunciation_overrides`. Both require `user_id`.
