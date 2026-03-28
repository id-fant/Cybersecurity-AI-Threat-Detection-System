def analyze(parsed_data):
    findings = []

    ports = parsed_data["open_ports"]

    if len(ports) > 5:
        findings.append("Possible port scan (many open ports)")

    if 22 in ports:
        findings.append("SSH exposed")

    if 80 in ports and 443 not in ports:
        findings.append("Unsecured HTTP (no HTTPS)")

    if not findings:
        findings.append("No obvious threats detected")

    return findings