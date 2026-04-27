# Cyber Agent

Cyber Agent is a small Python pipeline for turning Nmap scan output into security findings, an LLM-assisted risk summary, an optional Slack alert, and a saved SQLite alert record.

The current app is built around a simple flow:

1. Read a normal Nmap text report from `data/raw_logs/`.
2. Parse the target, open TCP ports, and service names.
3. Save the parsed result as JSON in `data/parsed_logs/`.
4. Apply rule-based checks for exposed SSH, HTTP without HTTPS, and unusually many open ports.
5. Classify the findings as `Low`, `Medium`, or `High`.
6. Ask Gemini for a short risk explanation, attack scenario, and fix.
7. Print the alert, optionally send it to Slack, and store it in `alerts.db`.

## Project Structure

```text
cyber-agent/
+-- actions/
|   +-- alert.py          # Sends Slack webhook alerts
|   +-- db.py             # Stores alert results in SQLite
+-- core/
|   +-- analyzer.py       # Rule-based finding generation
|   +-- decisionengine.py # Severity classification
|   +-- llmclient.py      # Gemini analysis client
+-- data/
|   +-- raw_logs/         # Input Nmap text reports
|   +-- parsed_logs/      # Generated parsed JSON reports
+-- parser/
|   +-- nmapp.py          # Nmap text parser
+-- main.py               # Pipeline entry point
+-- .env                  # Local environment variables
+-- alerts.db             # Generated SQLite alert database
```

## Requirements

- Python 3.10+
- A Gemini API key for LLM analysis
- A Slack incoming webhook URL if you want Slack alerts

Python packages used by the code:

```bash
pip install requests python-dotenv google-genai
```

`sqlite3` is part of the Python standard library.

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
SLACK_WEBHOOK_URL=your_slack_webhook_url
```

`SLACK_WEBHOOK_URL` is optional. If it is missing, the app prints a warning and continues without sending a Slack message.

## Usage

Add or generate an Nmap normal-output text file under `data/raw_logs/`.

Example Nmap command:

```bash
nmap -sS -oN data/raw_logs/sample.txt scanme.nmap.org
```

Run the default pipeline:

```bash
python main.py
```

By default, `main.py` processes:

```text
data/raw_logs/sample.txt
```

To process a different file, update the path passed to `run_pipeline()` in `main.py`, or call it from Python:

```python
from main import run_pipeline

run_pipeline("data/raw_logs/your_scan.txt")
```

## What Gets Generated

After a successful run, Cyber Agent creates or updates:

- `data/parsed_logs/<scan-name>.json` with parsed scan details
- `alerts.db` with an `alerts` table containing:
  - `ip`
  - `severity`
  - `findings`

The alert message is also printed to the console.

## Detection Rules

The current rule engine is intentionally lightweight:

- More than 5 open ports: `Possible port scan (many open ports)`
- Port 22 open: `SSH exposed`
- Port 80 open without port 443: `Unsecured HTTP (no HTTPS)`
- No matched rules: `No obvious threats detected`

Severity is assigned as:

- `High` when a port-scan finding is present
- `Medium` when unsecured HTTP is present
- `Low` when no obvious threats are detected
- `Medium` as the default fallback

## Notes

- The parser expects Nmap normal output with lines like `22/tcp open ssh`.
- The Gemini prompt asks for this strict response format: `Risk`, `Attack Scenario`, and `Fix`.
- The LLM client retries up to 3 times before returning a fallback response.
- Slack delivery is fire-and-forget; failed webhook responses are not currently retried or raised.
