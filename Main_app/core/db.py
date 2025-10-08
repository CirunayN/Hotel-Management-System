import sqlite3, os

def get_conn_to_reservastion(db_path="app_data.db") -> sqlite3.Connection:
    base = os.path.dirname(db_path)
    if base:
        os.makedirs(base, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

def get_conn_to_login(db_path="logins.db") -> sqlite3.Connection:
    base = os.path.dirname(db_path)
    if base:
        os.makedirs(base, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn
