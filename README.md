# Voice AI Study Coach

> Recruiter-facing public presentation generated from the verified local NALLAR portfolio package.

## 30-second summary

This project is presented around four questions: **what was built, how it was tested, what was measured, and what is not being claimed**.

## Evidence model

- Runnable implementation or portfolio artifact.
- Executable tests and/or quantitative evaluation.
- Reproducible local commands.
- Explicit limitations.

## Proof points

- STT adapter → Multi-Agent/RAG → TTS adapter.
- Study-session generation.
- Deterministic MockSTT/MockTTS evaluation.
- **10/10 tests passed.**

## Evidence boundary

Production ASR accuracy and production voice quality are not claimed.

---

## Reproduce locally

See the project files and original run notes below. Use the repository's own test/evaluation commands and inspect the generated evidence artifacts rather than relying on screenshots alone.


### Original run notes

# NALLAR Voice AI Study Coach

Run: `python voice_coach.py --topic "RAG evaluation"`

Test: `python -m unittest discover -s tests -v`


## Public claim boundary

This repository is published as an evidence-backed portfolio artifact. Test and evaluation results apply to the documented local/bundled scope. No production deployment, foundation-model training, or other unverified capability is implied.
