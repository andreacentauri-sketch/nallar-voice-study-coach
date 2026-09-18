# Voice AI Study Coach Design

Pipeline: audio reference -> STT adapter -> Multi-Agent evidence workflow -> TTS adapter. Bundled evaluation uses deterministic mock STT/TTS; optional macOS `say` provides local TTS. No production ASR accuracy is claimed.
