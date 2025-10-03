# Main_app/features/dashboard/view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QDateEdit, QCalendarWidget, QTableWidget, QMessageBox, QFrame
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
from Main_app.core.db import get_conn_to_reservastion
from Main_app.features.dashboard.func import (
    ensure_tables,
    fetch_reservations,
    populate_table,
    calculate_summary,
)


def build_dashboard_page() -> QWidget:
    return DashboardPage()


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Dashboard Page")
        self.conn = get_conn_to_reservastion()
        ensure_tables(self.conn)  # moved to func.py

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
        frame = QFrame()
        layout = QVBoxLayout(frame)
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label_value = QLabel(value)
        label_value.setFont(QFont("Arial", 16))
        label_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(label_value)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("background: #1670a5; border-radius: 8px; padding: 10px;")
        return frame, label_value

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

        rows = fetch_reservations(self.conn, start, end, room)
        populate_table(self.table, rows)

        summary = calculate_summary(self.conn, rows)
        for key, value in summary.items():
            self.cards[key].setText(value)
