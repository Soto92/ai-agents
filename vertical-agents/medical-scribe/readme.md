# Doctor AI – Medical Consultation Chatbot Using Google Gemini

Doctor AI is a text-based medical consultation assistant powered by Google Gemini AI.  
It allows users to simulate patient-doctor conversations, extract structured medical data, and store patient records locally.

---

## Features

- Text-based doctor-patient conversation input.
- Uses Google Gemini LLM to extract structured EHR data from conversation transcripts.
- Stores patient records in a local JSON file.
- Retrieve saved patient records.

---

## Requirements

- Python 3.8+
- Google Generative AI Python client
- A Google Gemini API key

---

## Installation

1. **Clone the repository** or save `doctor.py` to your working directory.

2. **Install dependencies**:

```bash
pip install google-generativeai python-dotenv
```

3. **Set up environment variables**:

Create a `.env` file in the same folder as `doctor.py` with your API key:

```env
API_KEY=your_google_gemini_api_key_here
```

---

## Usage

Run the script:

```bash
python doctor.py
```

The program will prompt you to paste a doctor-patient conversation transcript.
After processing, it will save the structured EHR entry locally and display it.

Type `exit` to quit the program.

---

## Demo

https://github.com/user-attachments/assets/288d7b85-478e-4f5a-9521-24e2d92a12f9

## Examples

### Example transcript input:

```
Dr: How old are you?
Patient: I'm 62 years old.
Patient: I've had a cough and fever for three days, temperature went up to 38.5.
Dr: Any medications?
Patient: I'm taking lisinopril 10 mg daily.
Patient: I'm allergic to penicillin.
```

### Output (structured JSON stored and displayed):

```json
{
  "patient": { "name": null, "age": 62, "gender": null },
  "vitals": {
    "temperature_c": 38.5,
    "heart_rate_bpm": null,
    "respiratory_rate_bpm": null,
    "blood_pressure": null
  },
  "symptoms": ["cough", "fever"],
  "medications": [
    { "name": "lisinopril", "dose": "10 mg", "frequency": "daily" }
  ],
  "allergies": ["penicillin"],
  "assessment": "Acute cough with fever; possible infectious etiology.",
  "plan": "Symptomatic treatment; consider chest X-ray if symptoms persist or worsen; consider antipyretic.",
  "follow_up": "Return if worse or follow-up in 48-72 hours."
}
```

---

## Notes

- The script saves EHR entries in `ehr_records.json` locally.
- This is a demo/prototype for educational use only — **not for clinical use**.
- Make sure your Google Gemini API key has the necessary permissions.

---

## License

MIT License
