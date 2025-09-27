
class Logins():
    def __init__(self, conn):
        self.conn = conn
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS reservation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        password TEXT NOT NULL
        )
        """)


