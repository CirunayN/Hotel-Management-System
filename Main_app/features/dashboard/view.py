# Main_app/features/dashboard/view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QDateEdit, QCalendarWidget, QTableWidget, QTableWidgetItem, QMessageBox,
    QFrame
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont, QColor, QBrush
from Main_app.core.db import get_conn_to_reservastion


def build_dashboard_page() -> QWidget:
    return DashboardPage()


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Dashboard Page")
        self.conn = get_conn_to_reservastion()
        self._ensure_table()

        # fonts
        title_font = QFont("Arial", 18, QFont.Weight.Bold)

        root = QVBoxLayout(self)

        title = QLabel("Dashboard")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        root.addWidget(title)

        # --- Summary Cards ---
        self.summary_layout = QHBoxLayout()
        root.addLayout(self.summary_layout)
        self.cards = {}
        for key in ["Total Reservations", "Expected Revenue", "Most Frequent Room"]:
            card = self._make_card(key, "0")
            self.cards[key] = card[1]
            self.summary_layout.addWidget(card[0])

        # --- Filters ---
        filters = QHBoxLayout()
        filters.addWidget(QLabel("Room Type:"))
        self.room_filter = QComboBox()
        self.room_filter.addItem("All")
        self.room_filter.addItems(["Single", "Double", "Suite"])
        filters.addWidget(self.room_filter)

        filters.addWidget(QLabel("Check-in from:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate())
        filters.addWidget(self.date_from)

        filters.addWidget(QLabel("to:"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate().addDays(3))
        filters.addWidget(self.date_to)

        self.btn_filter = QPushButton("Show Reserved Rooms")
        filters.addWidget(self.btn_filter)

        root.addLayout(filters)

        # --- Calendar + Table ---
        mid = QHBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumWidth(300)
        mid.addWidget(self.calendar, stretch=0)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Client Name", "Room Type", "Check-in", "Check-out"])
        self.table.horizontalHeader().setStretchLastSection(True)
        mid.addWidget(self.table, stretch=1)

        root.addLayout(mid)

        # Signals
        self.btn_filter.clicked.connect(self.on_filter)
        self.calendar.selectionChanged.connect(self.on_calendar_select)

        self.table.verticalHeader().setVisible(False)

        # initial load
        self.on_filter()

    def _make_card(self, title: str, value: str):
        """Create a simple summary card with title and value"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        lbl_title = QLabel(title)
        lbl_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        lbl_value = QLabel(value)
        lbl_value.setFont(QFont("Arial", 16))
        lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("background: #1670a5; border-radius: 8px; padding: 10px;")
        return frame, lbl_value

    def _ensure_table(self):
        cur = self.conn.cursor()
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
        self.conn.commit()

    def on_calendar_select(self):
        d = self.calendar.selectedDate()
        self.date_from.setDate(d)
        self.date_to.setDate(d)
        self.on_filter()

    def on_filter(self):
        start = self.date_from.date().toString("yyyy-MM-dd")
        end = self.date_to.date().toString("yyyy-MM-dd")

        if self.date_from.date() > self.date_to.date():
            QMessageBox.warning(self, "Invalid range", "Start date must be before or equal to end date.")
            return

        room = self.room_filter.currentText()
        params = (start, end)
        sql = """
        SELECT id, name, room_type, checkin, checkout FROM reservation
        WHERE NOT (checkout < ? OR checkin > ?)
        """
        if room != "All":
            sql += " AND room_type = ?"
            params = (start, end, room)

        rows = self.conn.execute(sql, params).fetchall()

        # --- Populate table ---
        self.table.setRowCount(len(rows))
        today = QDate.currentDate().toString("yyyy-MM-dd")
        for r, row in enumerate(rows):
            rid, name, rtype, checkin, checkout = row
            self.table.setItem(r, 0, QTableWidgetItem(name))
            self.table.setItem(r, 1, QTableWidgetItem(rtype))
            self.table.setItem(r, 2, QTableWidgetItem(checkin))
            self.table.setItem(r, 3, QTableWidgetItem(checkout))

            # --- Row coloring ---
            if checkin == today:
                for c in range(4):
                    self.table.item(r, c).setBackground(QBrush(QColor("#d4edda")))  # light green
            elif checkout < today:
                for c in range(4):
                    self.table.item(r, c).setBackground(QBrush(QColor("#f8d7da")))  # light red

        self.table.resizeColumnsToContents()

        # --- Update summary cards ---
        self.update_summary(rows)

    def update_summary(self, rows):
        total_res = len(rows)

        # Most frequent room type
        if rows:
            from collections import Counter
            room_types = [r[2] for r in rows]  # index 2 = room_type
            most_common = Counter(room_types).most_common(1)[0][0]
        else:
            most_common = "—"

        # Expected revenue (sum of service_orders totals for these reservations)
        ids = tuple(r[0] for r in rows)
        if ids:
            q = f"SELECT SUM(total) FROM service_orders WHERE reservation_id IN ({','.join('?'*len(ids))})"
            total_revenue = self.conn.execute(q, ids).fetchone()[0] or 0
        else:
            total_revenue = 0

        self.cards["Total Reservations"].setText(str(total_res))
        self.cards["Expected Revenue"].setText(f"₱{total_revenue}")
        self.cards["Most Frequent Room"].setText(most_common)
