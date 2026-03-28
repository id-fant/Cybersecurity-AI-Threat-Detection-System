from google import genai
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_llm_analysis(parsed_data, findings, severity):
    prompt = f"""
Respond in STRICT format:

Risk:
Attack Scenario:
Fix:

Data:
IP: {parsed_data['ip']}
Ports: {parsed_data['open_ports']}
Findings: {findings}
Severity: {severity}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            print(f"[Retry {attempt+1}] LLM failed:", e)
            time.sleep(2)

    return "LLM unavailable. Fallback response."