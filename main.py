from parser.nmapp import parse_nmap
from core.analyzer import analyze
from core.decisionengine import classify
from core.llmclient import get_llm_analysis
from actions.alert import send_slack_alert
from actions.db import save_result

def run_pipeline(file_path):
    parsed = parse_nmap(file_path)

    findings = analyze(parsed)
    severity = classify(findings)

    llm_output = get_llm_analysis(parsed, findings, severity)

    alert_message = f"""
🚨 ALERT: {severity}
IP: {parsed['ip']}
Findings: {findings}

{llm_output}
"""

    print(alert_message)

    send_slack_alert(alert_message)
    save_result(parsed["ip"], severity, findings)


if __name__ == "__main__":
    run_pipeline("data/raw_logs/sample.txt")