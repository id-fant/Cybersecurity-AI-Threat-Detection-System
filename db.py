import sqlite3

def save_result(ip, severity, findings):
    conn = sqlite3.connect("alerts.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            ip TEXT,
            severity TEXT,
            findings TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO alerts VALUES (?, ?, ?)",
        (ip, severity, str(findings))
    )

    conn.commit()
    conn.close()