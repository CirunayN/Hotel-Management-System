from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from collections import Counter


def make_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reservation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        number TEXT NOT NULL,
        room_type TEXT NOT NULL,
        checkin TEXT NOT NULL,
        checkout TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price INTEGER NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS service_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reservation_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (reservation_id) REFERENCES reservation(id),
        FOREIGN KEY (service_id) REFERENCES services(id)
    )
    """)
    conn.commit()


def fetch_reservations(conn, start, end, room):
    params = (start, end)
    sql = """
    SELECT id, name, room_type, checkin, checkout,price FROM reservation
    WHERE NOT (checkout < ? OR checkin > ?)
    """
    if room != "All":
        sql += " AND room_type = ?"
        params = (start, end, room)

    return conn.execute(sql, params).fetchall()


def show_table(table: QTableWidget, rows):
    table.setRowCount(len(rows))
    for r, row in enumerate(rows):
        rid, name, rtype, checkin, checkout, price = row
        table.setItem(r, 0, QTableWidgetItem(name))
        table.setItem(r, 1, QTableWidgetItem(rtype))
        table.setItem(r, 2, QTableWidgetItem(checkin))
        table.setItem(r, 3, QTableWidgetItem(checkout))
        table.setItem(r, 4, QTableWidgetItem(f"₱{price:,}"))


def calculate_summary(conn, rows):
    total_res = len(rows)
    room_revenue = sum(r[5] for r in rows) if rows else 0  # sum of room price (index 5)

    ids = tuple(r[0] for r in rows)
    if ids:
        q = f"SELECT SUM(total) FROM service_orders WHERE reservation_id IN ({','.join('?' * len(ids))})"
        service_revenue = conn.execute(q, ids).fetchone()[0] or 0
    else:
        service_revenue = 0

    total_revenue = room_revenue + service_revenue

    if rows:
        room_types = [r[2] for r in rows]
        most_common = Counter(room_types).most_common(1)[0][0]
    else:
        most_common = "—"

    return {
        "Total Reservations": str(total_res),
        "Expected Revenue": f"₱{total_revenue:,}",
        "Most Frequent Room": most_common,
    }


def search_user(conn, keyword: str):
    sql = """
    SELECT id, name, room_type, checkin, checkout,price
    FROM reservation
    WHERE name LIKE ? OR number LIKE ?
    """
    kw = f"%{keyword}%"
    return conn.execute(sql, (kw, kw)).fetchall()

