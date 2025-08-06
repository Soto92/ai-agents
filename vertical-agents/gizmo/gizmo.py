import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

# --- Setup the Gemini Client ---
try:
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    print("Please ensure you have set your API_KEY correctly.")
    exit()

# --- 1. THE "VERTICAL" PART: Specialized Knowledge & Actions ---

# This simulates a database of product information and customer data.
KNOWLEDGE_BASE = {
    "troubleshooting_steps": [
        "1. Unplug the GizmoTron 5000 and wait for 60 seconds.",
        "2. Plug it back in and wait for the status light to turn solid blue.",
        "3. Ensure your phone's Bluetooth is enabled and you are within 10 feet (3 meters).",
        "4. Try saying 'Hey Gizmo, reboot yourself'."
    ]
}

# This simulates a database of serial numbers and their warranty status.
SERIAL_NUMBERS = {
    "GZ5K-112358": {"status": "Active", "expires": "2026-08-15"},
    "GZ5K-132134": {"status": "Expired", "expires": "2024-03-20"},
    "GZ5K-213455": {"status": "Active", "expires": "2025-11-01"},
}

# These are the specific actions our agent can perform.
def check_warranty(serial_number):
    """Checks the warranty status for a given serial number."""
    if not serial_number:
        return "I need a serial number to check the warranty. It looks like 'GZ5K-XXXXXX'."
    info = SERIAL_NUMBERS.get(serial_number)
    if info:
        return f"Warranty for {serial_number} is {info['status']}. It expires/expired on {info['expires']}."
    else:
        return f"Sorry, I could not find a record for serial number {serial_number}."

def provide_troubleshooting():
    """Provides a list of troubleshooting steps."""
    steps = "\n".join(KNOWLEDGE_BASE["troubleshooting_steps"])
    return f"Let's try some basic troubleshooting:\n{steps}"

def create_ticket(serial_number):
    """Simulates creating a support ticket."""
    if not serial_number:
        return "I can create a ticket, but I'll need the device's serial number first."
    # In a real app, this would interact with a ticketing system (e.g., Zendesk, Jira API).
    ticket_id = "TICKET-" + str(hash(serial_number))[-6:]
    return f"I've created a support ticket for you. Your ticket ID is {ticket_id}. A human agent will contact you within 24 hours."


# --- 2. THE "AI" PART: The Agent's Brain ---

class GizmoTronAgent:
    """The AI agent that understands user queries."""
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-2.0-flash')

    def analyze_query(self, user_query):
        """Uses the LLM to determine user intent and extract information."""
        
        prompt = f"""
        You are a helpful and concise customer support AI for a fictional product called the "GizmoTron 5000". 
        Your task is to analyze the user's request and respond in a specific JSON format.

        Based on the user's query, identify exactly one of the following intents:
        - "check_warranty": User wants to know their warranty status.
        - "troubleshoot": User is having a problem and needs help.
        - "create_ticket": User explicitly asks to create a support ticket or case.
        - "greet": User says hello or thank you.
        - "unknown": The user's request is not related to any of the above.
        
        Also, extract the serial number if the user provides one. The serial number format is "GZ5K-XXXXXX".

        Return ONLY a valid JSON object with two keys: "intent" and "serial_number".
        The value for "serial_number" must be a string, or null if it's not present.

        User Query: "{user_query}"
        
        JSON Response:
        """
        try:
            response = self.model.generate_content(prompt)
            # Clean up the response to ensure it's valid JSON
            cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(cleaned_response)
        except (json.JSONDecodeError, AttributeError, ValueError) as e:
            print(f"--- [Error] Could not parse LLM response: {e} ---")
            return {"intent": "unknown", "serial_number": None}

# --- 3. THE "ROUTER": Connecting the Brain to the Actions ---

def main():
    """The main function to run the agent."""
    agent = GizmoTronAgent()
    print("Welcome to GizmoTron 5000 Support! How can I help you? (Type 'exit' to quit)")

    # GET MODELS
    # for model in genai.list_models():
    #     print(model.name, model.supported_generation_methods)

    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Thank you for contacting GizmoTron Support. Goodbye!")
            break
            
        try:
            # 1. AI brain analyzes the query
            analysis = agent.analyze_query(user_input)
            intent = analysis.get("intent")
            serial_number = analysis.get("serial_number")
            
            print(f"--- (Debug: Intent='{intent}', Serial='{serial_number}') ---")

            # 2. Router directs to the correct action
            if intent == "check_warranty":
                    response = check_warranty(serial_number)
            elif intent == "troubleshoot":
                    response = provide_troubleshooting()
            elif intent == "create_ticket":
                    response = create_ticket(serial_number)
            elif intent == "greet":
                    response = "Hello! How can I assist you with your GizmoTron 5000 today?"
            else: # 'unknown'
                    response = "I'm sorry, I'm not sure how to help with that. You can ask me to check a warranty, provide troubleshooting steps, or create a ticket."
                
            print(f"\n🤖: {response}\n")

        except Exception as e:
            if "429" in str(e):
                print("\n🤖: You exceeded your current quota.\n")
            else:
                print(f"\n🤖: Sorry, there was an error processing your request: {e}\n")

if __name__ == "__main__":
    main()