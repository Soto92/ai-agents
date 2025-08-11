# GizmoTron 5000 🤖

GizmoTron 5000 is an AI-powered support assistant built using the Google Generative AI API (Gemini Pro). It interprets user queries, classifies intents, and responds with predefined actions such as checking warranty status, providing troubleshooting steps, or creating support tickets.

## 🤖 What is GizmoTron 5000?

GizmoTron 5000 is a **vertical agent**, meaning it is specialized in a narrow domain—in this case, technical support for the GizmoTron 5000 device. It has deep knowledge and predefined actions in this area, such as:

- Checking warranty status based on serial numbers
- Providing step-by-step troubleshooting instructions
- Creating support tickets for issues reported by users

Unlike general-purpose agents, a vertical agent focuses on solving specific problems deeply and efficiently.

---

## Demo

https://github.com/user-attachments/assets/0a6a69cc-8e11-4032-9ae5-81409446e2f3

## ✅ Requirements

- Python 3.8+
- [uv](https://astral.sh/docs/uv/)

---

## 🚀 Setup Instructions

### 1. Create a virtual environment in gizmo folder

```bash
uv venv
uv venv activate
```

### 2. Install dependencies

You can install from `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

or

```
.\.venv\Scripts\Activate.ps1
```

Or install directly:

```bash
uv pip install python-dotenv requests
```

### 3. Set your API key

Create a `.env` file:

```
API_KEY=your_google_api_key
```

Get it from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

---

## 📁 Project Structure

```
your_project/
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🚀 Features

- Natural language understanding using **Gemini Pro**
- Intent detection and classification
- Modular actions:
  - `check_warranty`
  - `troubleshoot`
  - `create_ticket`
- CLI-based chat interface

---

## 🧠 How It Works

When a user types a query, the `GizmoTronAgent`:

1. Sends the query to Gemini Pro with a custom prompt.
2. Extracts a JSON structure containing:
   - `intent`
   - `action`
   - `confidence`
3. Executes the corresponding Python method for the action.

## ▶️ Running

```bash
python gizmo.py
```

Then, chat with the agent:

```
Welcome to GizmoTron 5000 Support! How can I help you?
> my printer is not turning on
```

### Example Questions & Commands for GizmoTron 5000

- Warranty Check

  - “Can you check the warranty for serial number GZ5K-112358?”
  - “Is my GizmoTron under warranty? Serial: GZ5K-213455”
  - “Check warranty GZ5K-132134”

- Troubleshooting Help

  - “My GizmoTron 5000 is not turning on.”
  - “How do I fix Bluetooth connection issues?”
  - “It won’t reboot, what should I do?”
  - “Troubleshoot my GizmoTron”

- Create Support Ticket

  - “I want to create a support ticket for serial GZ5K-112358.”
  - “Please open a ticket, my device is broken.”
  - “Create a support case for me.”

- Greetings & Politeness

  - “Hello”
  - “Thanks for your help!”
  - “Hi there”

- Unknown or Random Questions

  - “What’s the weather today?”
  - “Tell me a joke.”
  - “Who won the game yesterday?”

---

## 📦 Example Output from Gemini

Gemini will return something like:

```json
{
  "intent": "create_ticket",
  "action": "troubleshoot",
  "confidence": 0.95
}
```

---

## ✨ Credits

Built with ❤️ using:

- [Google Gemini API](https://ai.google.dev)
- Python 3.11
- `google-generativeai` SDK

## 📝 License

MIT – do whatever you want.
