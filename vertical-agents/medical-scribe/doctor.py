import os
import json
import time
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise SystemExit("Please set API_KEY in your .env file")

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    raise SystemExit(f"Failed to configure Gemini client: {e}")

# --- Simple persistent store for demo (JSON file) ---
DB_FILE = "ehr_records.json"

def load_records():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []

def save_record(record):
    records = load_records()
    records.append(record)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# --- Domain actions (vertical part) ---
def create_ehr_entry(parsed):
    """
    Simulate storing an EHR entry. `parsed` is the JSON object returned by the model.
    """
    record = {
        "id": int(time.time() * 1000),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ehr": parsed
    }
    save_record(record)
    return record

def list_records():
    return load_records()

# --- The agent which uses Gemini to parse transcripts into structured EHR JSON ---
class MedicalScribeAgent:
    def __init__(self, model_name="models/gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)

        self.system_prompt = """
You are a concise medical scribe assistant. Given a doctor-patient conversation transcript, extract structured
EHR information and return ONLY a JSON object (no extra text) with the exact fields specified below.

Required JSON schema (fields must exist; use null or empty arrays when unknown):
{
  "patient": {
    "name": string|null,
    "age": integer|null,
    "gender": "male"|"female"|null
  },
  "vitals": {
    "temperature_c": number|null,
    "heart_rate_bpm": integer|null,
    "respiratory_rate_bpm": integer|null,
    "blood_pressure": string|null  // e.g. "120/80 mmHg"
  },
  "symptoms": [string],
  "medications": [{"name": string, "dose": string|null, "frequency": string|null}],
  "allergies": [string],
  "assessment": string|null,
  "plan": string|null,
  "follow_up": string|null
}

Important:
- Return JSON only. No markdown, no commentary, no code fences.
- Use ISO-like formats where applicable. Use null for missing numeric values.
- Be conservative: if unsure, set fields to null or [] rather than guessing specifics.
"""
        self.example_pair_1 = {
            "transcript": (
                "Dr: How old are you? Patient: I'm 62 years old. "
                "Patient: I've had a cough and fever for three days, temperature went up to 38.5. "
                "Dr: Any medications? Patient: I'm taking lisinopril 10 mg daily. "
                "Patient: I'm allergic to penicillin."
            ),
            "json": {
                "patient": {"name": None, "age": 62, "gender": None},
                "vitals": {"temperature_c": 38.5, "heart_rate_bpm": None, "respiratory_rate_bpm": None, "blood_pressure": None},
                "symptoms": ["cough", "fever"],
                "medications": [{"name": "lisinopril", "dose": "10 mg", "frequency": "daily"}],
                "allergies": ["penicillin"],
                "assessment": "Acute cough with fever; possible infectious etiology.",
                "plan": "Symptomatic treatment; consider chest X-ray if symptoms persist or worsen; consider antipyretic.",
                "follow_up": "Return if worse or follow-up in 48-72 hours."
            }
        }

        self.example_pair_2 = {
            "transcript": (
                "Patient: Hi, I'm Maria Silva, I'm 29. Doctor: What brings you in? "
                "Patient: I've had headaches and dizziness for two weeks. No meds. "
                "Doctor: Any known allergies? Patient: No."
            ),
            "json": {
                "patient": {"name": "Maria Silva", "age": 29, "gender": None},
                "vitals": {"temperature_c": None, "heart_rate_bpm": None, "respiratory_rate_bpm": None, "blood_pressure": None},
                "symptoms": ["headache", "dizziness"],
                "medications": [],
                "allergies": [],
                "assessment": "Chronic headaches and dizziness; differential includes tension headache, migraine, or vestibular causes.",
                "plan": "Recommend neurological exam, consider migraine therapy, advise hydration and sleep hygiene.",
                "follow_up": "Neurology referral if no improvement in 2 weeks."
            }
        }

    def _build_prompt(self, transcript):
        prompt = self.system_prompt.strip() + "\n\n"
       
        prompt += "Example Transcript 1:\n" + self.example_pair_1["transcript"] + "\n\n"
        prompt += "Example Output 1 JSON:\n" + json.dumps(self.example_pair_1["json"], ensure_ascii=False) + "\n\n"
       
        prompt += "Example Transcript 2:\n" + self.example_pair_2["transcript"] + "\n\n"
        prompt += "Example Output 2 JSON:\n" + json.dumps(self.example_pair_2["json"], ensure_ascii=False) + "\n\n"
       
        prompt += "Transcript to parse:\n" + transcript + "\n\n"
        prompt += "Now produce the JSON according to the schema above."
        return prompt

    def parse_transcript(self, transcript, max_retries=1):
        prompt = self._build_prompt(transcript)
        try:
            resp = self.model.generate_content(prompt)
            text = resp.text.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(text)
            return parsed
        except Exception as e:
            if max_retries > 0:
                fallback_prompt = (
                    "Return only a single-line JSON object following this schema (no explanations). "
                    "If you cannot determine a field, use null or empty arrays.\n\n" + prompt
                )
                try:
                    resp2 = self.model.generate_content(fallback_prompt)
                    text2 = resp2.text.strip().replace("```json", "").replace("```", "").strip()
                    return json.loads(text2)
                except Exception as e2:
                    print(f"[ERROR] LLM parse failed: {e2}")
                    return None
            else:
                print(f"[ERROR] LLM parse failed: {e}")
                return None

# --- CLI / Router ---
def main():
    agent = MedicalScribeAgent()
    print("Medical Scribe AI (transcript -> structured EHR). Type 'exit' to quit.\n")

    while True:
        print("Paste the doctor-patient transcript (single line or multiline). End with an empty line:")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                return
            if line.strip() == "":
                break
            lines.append(line)
        transcript = "\n".join(lines).strip()
        if not transcript:
            continue
        if transcript.lower() in ("exit", "quit", "bye"):
            print("Goodbye.")
            break

        parsed = agent.parse_transcript(transcript)
        if not parsed:
            print("Failed to parse transcript. Try rephrasing or use a shorter clip.")
            continue

        record = create_ehr_entry(parsed)
        print("\n--- EHR entry saved ---")
        print(json.dumps(record, ensure_ascii=False, indent=2))
        print("------------------------\n")

        print("Actions: [L]ist records, [C]ontinue, [E]xit")
        a = input("> ").strip().lower()
        if a == "l":
            print(json.dumps(list_records(), ensure_ascii=False, indent=2))
        if a in ("e", "exit"):
            break

if __name__ == "__main__":
    main()
