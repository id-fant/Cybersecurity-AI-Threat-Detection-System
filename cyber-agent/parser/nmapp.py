import re
import json
import os

def parse_nmap(file_path):
    with open(file_path, "r") as f:
        data = f.read()

    ip_match = re.search(r"Nmap scan report for ([^\n]+)", data)
    ports = re.findall(r"(\d+)/tcp\s+open\s+([\w\-]+)", data)

    parsed = {
        "ip": ip_match.group(1).strip() if ip_match else "unknown",
        "open_ports": [int(p[0]) for p in ports],
        "services": [p[1].strip() for p in ports],
        "raw": data
    }

    os.makedirs("data/parsed_logs", exist_ok=True)
    filename = os.path.basename(file_path).replace(".txt", ".json")
    output_path = f"data/parsed_logs/{filename}"

    with open(output_path, "w") as f:
        json.dump(parsed, f, indent=4)

    print(f"[✔] Parsed saved → {output_path}")

    return parsed