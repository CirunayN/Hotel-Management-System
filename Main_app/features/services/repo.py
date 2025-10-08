from PyQt6.QtCore import QDateTime


class ServicesFunc:
    def __init__(self, conn):
        self.conn = conn

    def create_tables(self):
        cur = self.conn.cursor()
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
            created_at TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def add_service(self, name: str, category: str, price: int):
        cur = self.conn.execute(
            "INSERT INTO services (name, category, price) VALUES (?, ?, ?)",
            (name, category, price),
        )
        self.conn.commit()
        return cur.lastrowid

    def list_services(self):
        return self.conn.execute(
            "SELECT id, name, category, price FROM services ORDER BY id DESC"
        ).fetchall()

    def delete_service_and_orders(self, service_id: int):
        self.conn.execute("DELETE FROM service_orders WHERE service_id=?", (service_id,))
        self.conn.execute("DELETE FROM services WHERE id=?", (service_id,))
        self.conn.commit()

    def list_reservations(self):
        return self.conn.execute(
            "SELECT id, name, checkin, checkout FROM reservation ORDER BY id DESC"
        ).fetchall()

    def assign_service(self, reservation_id: int, service_id: int, qty: int):
        price = int(
            self.conn.execute("SELECT price FROM services WHERE id=?", (service_id,))
            .fetchone()[0]
        )
        total = price * qty

        cur = self.conn.execute(
            "SELECT id, quantity, total FROM service_orders WHERE reservation_id=? AND service_id=?",
            (reservation_id, service_id),
        ).fetchone()

        if cur:
            oid, old_qty, old_total = cur
            new_qty = old_qty + qty
            new_total = new_qty * price
            self.conn.execute(
                "UPDATE service_orders SET quantity=?, total=? WHERE id=?",
                (new_qty, new_total, oid),
            )
        else:
            created_date = QDateTime.currentDateTime().toString("yyyy-MM-dd")
            self.conn.execute(
                "INSERT INTO service_orders (reservation_id, service_id, quantity, total, created_at) VALUES (?,?,?,?,?)",
                (reservation_id, service_id, qty, total, created_date),
            )
        self.conn.commit()

    def list_orders(self):
        return self.conn.execute("""
            SELECT r.id AS reservation_id,
                   r.name AS client_name,
                   GROUP_CONCAT(s.name || ' (x' || o.quantity || ')', ', ') AS services,
                   SUM(o.total) AS total
            FROM service_orders o
            LEFT JOIN reservation r ON r.id = o.reservation_id
            LEFT JOIN services s ON s.id = o.service_id
            GROUP BY r.id, r.name
            ORDER BY r.id DESC
        """).fetchall()

    def remove_order(self, reservation_id: int):
        self.conn.execute("DELETE FROM service_orders WHERE reservation_id=?", (reservation_id,))
        self.conn.commit()
