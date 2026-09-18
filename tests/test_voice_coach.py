from __future__ import annotations
import json, os, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from voice_coach import MockSTT, MockTTS, MacSayTTS, StudyPlanner, VoiceStudyCoach
class T(unittest.TestCase):
    def coach(self): return VoiceStudyCoach(MockSTT({"a1":"How does retrieval evaluation use recall and MRR?"}),MockTTS())
    def test_01_stt(self): self.assertIn("recall",MockSTT({"x":"recall MRR"}).transcribe("x"))
    def test_02_missing(self):
        with self.assertRaises(KeyError): MockSTT({}).transcribe("x")
    def test_03_cards(self): self.assertEqual(len(StudyPlanner().cards_from_topic("MCP")),3)
    def test_04_empty(self):
        with self.assertRaises(ValueError): StudyPlanner().cards_from_topic(" ")
    def test_05_pipeline(self):
        o=self.coach().handle_audio("a1"); self.assertEqual(o["agent_roles"],["planner","researcher","evaluator","synthesizer"]); self.assertTrue(o["tts"]["spoken"]); self.assertFalse(o["raw_transcript_persisted"])
    def test_06_cites(self): self.assertGreaterEqual(len(self.coach().handle_audio("a1")["cited_doc_ids"]),1)
    def test_07_tts(self):
        o=MockTTS().speak("hello"); self.assertTrue(o["spoken"]); self.assertEqual(o["text_length"],5); self.assertEqual(len(o["text_sha256"]),64)
    def test_08_say(self): self.assertIsInstance(MacSayTTS().available(),bool)
    def test_09_cli(self):
        p=subprocess.run([sys.executable,str(ROOT/"voice_coach.py"),"--topic","MCP"],capture_output=True,text=True,timeout=30,env=os.environ.copy())
        self.assertEqual(p.returncode,0); self.assertEqual(json.loads(p.stdout)["study_session"]["card_count"],3)
    def test_10_no_network(self):
        t=(ROOT/"voice_coach.py").read_text().lower(); self.assertNotIn("import requests",t); self.assertNotIn("import socket",t)
if __name__=="__main__": unittest.main(verbosity=2)
