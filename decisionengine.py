def classify(findings):
    if any("port scan" in f for f in findings):
        return "High"

    if any("Unsecured HTTP" in f for f in findings):
        return "Medium"

    if any("No obvious" in f for f in findings):
        return "Low"

    return "Medium"