#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, shutil, subprocess
from pathlib import Path

def agent_root():
    raw=os.environ.get("NALLAR_AGENT_PACKAGE")
    return Path(raw).expanduser().resolve() if raw else (Path(__file__).resolve().parents[1]/"04_MULTI_AGENT_SYSTEM").resolve()
def load_agent():
    p=agent_root()/"agent_system.py"
    if not p.is_file(): raise FileNotFoundError(str(p))
    spec=importlib.util.spec_from_file_location("nallar_g3_agent",p)
    if spec is None or spec.loader is None: raise RuntimeError("unable to load agent module")
    m=importlib.util.module_from_spec(spec); __import__("sys").modules[spec.name]=m; spec.loader.exec_module(m); return m

class MockSTT:
    def __init__(self,m): self.m=dict(m)
    def transcribe(self,a):
        if a not in self.m: raise KeyError("unknown audio_ref")
        return self.m[a]
class MockTTS:
    def __init__(self): self.calls=[]
    def speak(self,text):
        self.calls.append(text); return {"spoken":True,"text_sha256":hashlib.sha256(text.encode()).hexdigest(),"text_length":len(text)}
class MacSayTTS:
    def __init__(self): self.binary=shutil.which("say")
    def available(self): return bool(self.binary)
    def speak(self,text):
        if not self.binary: return {"spoken":False,"reason":"say_not_available"}
        p=subprocess.run([self.binary,text],capture_output=True,text=True,timeout=30)
        return {"spoken":p.returncode==0,"exit_code":p.returncode,"stderr_length":len(p.stderr or "")}
class StudyPlanner:
    def cards_from_topic(self,topic):
        topic=topic.strip()
        if not topic: raise ValueError("topic required")
        return [{"question":f"Define {topic}.","answer":f"Ground the definition of {topic} in retrieved evidence."},
                {"question":f"Name one engineering tradeoff in {topic}.","answer":"Discuss accuracy, latency, privacy, reproducibility, or complexity."},
                {"question":f"How would you evaluate {topic}?","answer":"Use explicit tests, metrics, failure cases, and evidence boundaries."}]
class VoiceStudyCoach:
    def __init__(self,stt,tts):
        self.stt=stt; self.tts=tts; self.planner=StudyPlanner(); self.orchestrator=load_agent().MultiAgentOrchestrator()
    def handle_audio(self,a):
        tr=self.stt.transcribe(a); result=self.orchestrator.run(tr); ans=result["synthesis"]["answer"]; spoken=self.tts.speak(ans)
        return {"audio_ref_sha256":hashlib.sha256(a.encode()).hexdigest(),"transcript_sha256":hashlib.sha256(tr.encode()).hexdigest(),
                "transcript_length":len(tr),"raw_transcript_persisted":False,"agent_roles":result["roles"],
                "cited_doc_ids":result["synthesis"]["cited_doc_ids"],"abstained":result["synthesis"]["abstained"],"tts":spoken}
    def study_session(self,topic):
        cards=self.planner.cards_from_topic(topic)
        return {"topic_sha256":hashlib.sha256(topic.encode()).hexdigest(),"card_count":len(cards),"cards":cards}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--topic",default="RAG evaluation"); ap.add_argument("--transcript",default="How does retrieval evaluation use recall and MRR?")
    a=ap.parse_args(); c=VoiceStudyCoach(MockSTT({"demo":a.transcript}),MockTTS())
    print(json.dumps({"voice_demo":c.handle_audio("demo"),"study_session":c.study_session(a.topic),"mac_say_available":MacSayTTS().available()},indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
