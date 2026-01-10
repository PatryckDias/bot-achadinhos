import sqlite3

conn = sqlite3.connect("sent.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS sent (
    id TEXT PRIMARY KEY
)
""")

def already_sent(pid):
    c.execute("SELECT 1 FROM sent WHERE id=?", (pid,))
    return c.fetchone() is not None

def mark_sent(pid):
    c.execute("INSERT OR IGNORE INTO sent VALUES (?)", (pid,))
    conn.commit()
