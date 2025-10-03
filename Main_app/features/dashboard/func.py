# Main_app/features/dashboard/func.py
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from collections import Counter


def ensure_tables(conn):
    """Create necessary tables if not exist"""
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


def fetch_reservations(conn, start, end, room_filter):
    params = (start, end)
    sql = """
    SELECT id, name, room_type, checkin, checkout FROM reservation
    WHERE NOT (checkout < ? OR checkin > ?)
    """
    if room_filter != "All":
        sql += " AND room_type = ?"
        params = (start, end, room_filter)

    return conn.execute(sql, params).fetchall()


def populate_table(table: QTableWidget, rows):
    """Populate the reservation table with data and color rows."""
    table.setRowCount(len(rows))
    today = QDate.currentDate().toString("yyyy-MM-dd")

    for r, row in enumerate(rows):
        rid, name, rtype, checkin, checkout = row
        table.setItem(r, 0, QTableWidgetItem(name))
        table.setItem(r, 1, QTableWidgetItem(rtype))
        table.setItem(r, 2, QTableWidgetItem(checkin))
        table.setItem(r, 3, QTableWidgetItem(checkout))

        # --- Row coloring ---
        if checkin == today:
            for c in range(4):
                table.item(r, c).setBackground(QBrush(QColor("#d4edda")))  # light green
        elif checkout < today:
            for c in range(4):
                table.item(r, c).setBackground(QBrush(QColor("#f8d7da")))  # light red

    table.resizeColumnsToContents()


def calculate_summary(conn, rows):
    total_res = len(rows)
    if rows:
        room_types = [r[2] for r in rows]  # index 2 = room_type
        most_common = Counter(room_types).most_common(1)[0][0]
    else:
        most_common = "—"

    # Expected revenue
    ids = tuple(r[0] for r in rows)
    if ids:
        q = f"SELECT SUM(total) FROM service_orders WHERE reservation_id IN ({','.join('?'*len(ids))})"
        total_revenue = conn.execute(q, ids).fetchone()[0] or 0
    else:
        total_revenue = 0

    return {
        "Total Reservations": str(total_res),
        "Expected Revenue": f"₱{total_revenue}",
        "Most Frequent Room": most_common,
    }
