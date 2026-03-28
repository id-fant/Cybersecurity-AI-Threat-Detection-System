import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_slack_alert(message):
    webhook = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook:
        print("[!] No Slack webhook configured")
        return

    requests.post(webhook, json={"text": message})