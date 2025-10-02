# Main_app/features/services/view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import QDateTime
from Main_app.core.db import get_conn_to_reservastion
from Main_app.core.data import Reservation
import sqlite3


def build_services_page() -> QWidget:
    return ServicesPage()


class ServicesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Services Page")
        self.conn = get_conn_to_reservastion()
        self._create_tables()

        root = QVBoxLayout(self)

        title = QLabel("Services")
        title.setStyleSheet("font-weight: bold; font-size: 15px;")
        root.addWidget(title)

        form = QHBoxLayout()
        form.addWidget(QLabel("Service name:"))
        self.svc_name = QLineEdit()
        form.addWidget(self.svc_name)

        form.addWidget(QLabel("Category:"))
        self.svc_cat = QComboBox()
        self.svc_cat.addItems(["Laundry", "Food", "Cleaning", "Other"])
        form.addWidget(self.svc_cat)

        form.addWidget(QLabel("Price (₱): "))
        self.svc_price = QSpinBox()
        self.svc_price.setRange(0, 100000)
        form.addWidget(self.svc_price)

        self.btn_add_service = QPushButton("Add Service")
        form.addWidget(self.btn_add_service)
        self.btn_delete_service = QPushButton("Delete Selected Service")
        form.addWidget(self.btn_delete_service)

        root.addLayout(form)

        self.table_services = QTableWidget(0, 4)
        self.table_services.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price"])
        root.addWidget(self.table_services)

        assign_layout = QHBoxLayout()
        assign_layout.addWidget(QLabel("Reservation:"))
        self.reservation_select = QComboBox()
        assign_layout.addWidget(self.reservation_select)

        assign_layout.addWidget(QLabel("Service:"))
        self.service_select = QComboBox()
        assign_layout.addWidget(self.service_select)

        assign_layout.addWidget(QLabel("Quantity:"))
        self.qty = QSpinBox()
        self.qty.setRange(1, 100)
        assign_layout.addWidget(self.qty)

        self.btn_assign = QPushButton("Assign Service")
        assign_layout.addWidget(self.btn_assign)

        self.btn_delete_order = QPushButton("Delete Selected Order")
        assign_layout.addWidget(self.btn_delete_order)

        root.addLayout(assign_layout)

        self.table_orders = QTableWidget(0, 4)
        self.table_orders.setHorizontalHeaderLabels(
            ["Reservation ID", "Client Name", "Service","Total"]
        )
        self.table_orders.resizeColumnsToContents()
        root.addWidget(self.table_orders)

        self.btn_add_service.clicked.connect(self.add_service)
        self.btn_delete_service.clicked.connect(self.delete_selected_service)
        self.btn_assign.clicked.connect(self.assign_service)
        self.btn_delete_order.clicked.connect(self.delete_selected_order)

        self.refresh_services()
        self.refresh_reservations()
        self.refresh_orders()

    def _create_tables(self):
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

    def add_service(self):
        name = self.svc_name.text().strip()
        cat = self.svc_cat.currentText()
        price = int(self.svc_price.value())
        if not name:
            QMessageBox.warning(self, "Validation", "Service name is required")
            return
        cur = self.conn.execute("INSERT INTO services (name, category, price) VALUES (?, ?, ?)", (name, cat, price))
        self.conn.commit()
        self.svc_name.clear()
        self.svc_price.setValue(0)
        self.refresh_services()

    def refresh_services(self):
        rows = self.conn.execute("SELECT id, name, category, price FROM services ORDER BY id DESC").fetchall()
        self.table_services.setRowCount(len(rows))
        self.service_select.clear()
        for r, row in enumerate(rows):
            sid, name, cat, price = row
            self.table_services.setItem(r, 0, QTableWidgetItem(str(sid)))
            self.table_services.setItem(r, 1, QTableWidgetItem(name))
            self.table_services.setItem(r, 2, QTableWidgetItem(cat))
            self.table_services.setItem(r, 3, QTableWidgetItem(str(price)))
            self.service_select.addItem(f"{name} (₱{price})", sid)
        self.table_services.resizeColumnsToContents()

    def delete_selected_service(self):
        row = self.table_services.currentRow()
        if row < 0:
            return
        sid = int(self.table_services.item(row, 0).text())
        cnt = self.conn.execute("SELECT COUNT(*) FROM service_orders WHERE service_id=?", (sid,)).fetchone()[0]
        if cnt > 0:
            QMessageBox.warning(self, "Cannot delete", "Service has existing orders; delete orders first.")
            return
        self.conn.execute("DELETE FROM services WHERE id=?", (sid,))
        self.conn.commit()
        self.refresh_services()

    def refresh_reservations(self):
        rows = self.conn.execute("SELECT id, name, checkin, checkout FROM reservation ORDER BY id DESC").fetchall()
        self.reservation_select.clear()
        for row in rows:
            rid, name, ci, co = row
            self.reservation_select.addItem(f"{rid} — {name} ({ci}→{co})", rid)

    def assign_service(self):
        if self.reservation_select.count() == 0 or self.service_select.count() == 0:
            QMessageBox.warning(self, "Validation", "Need reservation and service selected.")
            return
        rid = int(self.reservation_select.currentData())
        sid = int(self.service_select.currentData())
        qty = int(self.qty.value())
        price = int(self.conn.execute("SELECT price FROM services WHERE id=?", (sid,)).fetchone()[0])
        total = price * qty


        cur = self.conn.execute(
            "SELECT id, quantity, total FROM service_orders WHERE reservation_id=? AND service_id=?",
            (rid, sid)
        ).fetchone()

        if cur:
            oid, old_qty, old_total = cur
            new_qty = old_qty + qty
            new_total = new_qty * price
            self.conn.execute(
                "UPDATE service_orders SET quantity=?, total=? WHERE id=?",
                (new_qty, new_total, oid)
            )
        else:
            # new assignment
            created_at = QDateTime.currentDateTime().toString("yyyy-MM-dd")
            self.conn.execute(
                "INSERT INTO service_orders (reservation_id, service_id, quantity, total, created_at) VALUES (?,?,?,?,?)",
                (rid, sid, qty, total, created_at),
            )
        self.conn.commit()
        self.refresh_orders()


    def refresh_orders(self):
        rows = self.conn.execute("""
                                 SELECT r.id                                                     AS reservation_id,
                                        r.name                                                   AS client_name,
                                        GROUP_CONCAT(s.name || ' (x' || o.quantity || ')', ', ') AS services,
                                        SUM(o.total)                                             AS total
                                 FROM service_orders o
                                          LEFT JOIN reservation r ON r.id = o.reservation_id
                                          LEFT JOIN services s ON s.id = o.service_id
                                 GROUP BY r.id, r.name
                                 ORDER BY r.id DESC
                                 """).fetchall()

        self.table_orders.setRowCount(len(rows))
        for r, row in enumerate(rows):
            rid, client, services, total = row
            self.table_orders.setItem(r, 0, QTableWidgetItem(str(rid)))
            self.table_orders.setItem(r, 1, QTableWidgetItem(client or "—"))
            self.table_orders.setItem(r, 2, QTableWidgetItem(services or "—"))
            self.table_orders.setItem(r, 3, QTableWidgetItem(str(total or 0)))

    def delete_selected_order(self):
        row = self.table_orders.currentRow()
        if row < 0:
            return
        oid = int(self.table_orders.item(row, 0).text())
        self.conn.execute("DELETE FROM service_orders WHERE id=?", (oid,))
        self.conn.commit()
        self.refresh_orders()
