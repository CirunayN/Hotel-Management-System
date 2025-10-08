# dashboard.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QDateEdit, QTableWidget, QMessageBox, QFrame, QLineEdit, QGroupBox
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHeaderView

from Main_app.core.db import get_conn_to_reservastion
from Main_app.features.dashboard.repo import (
    make_tables,
    fetch_reservations,
    show_table,
    calculate_summary,
    search_user,
)
from Main_app.core.stylesheet import StyleShesh


def build_dashboard_page() -> QWidget:
    return DashboardPage()


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Dashboard Page")
        self.conn = get_conn_to_reservastion()
        make_tables(self.conn)

        # Apply global page style - ONLY ONCE
        self.setStyleSheet(StyleShesh.Page)

        root = QVBoxLayout(self)
        root.setSpacing(15)
        root.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Dashboard")
        title.setStyleSheet(StyleShesh.TitleBanner)
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        root.addWidget(title)

        # Summary cards
        self.summary_layout = QHBoxLayout()
        root.addLayout(self.summary_layout)
        self.cards = {}
        for key in ["Total Reservations", "Expected Revenue", "Most Frequent Room"]:
            card = self._make_card(key, "0")
            self.cards[key] = card[1]
            self.summary_layout.addWidget(card[0])

        # Filters Group Box
        filters_group = QGroupBox("Filter Reservations")
        filters_group.setStyleSheet(StyleShesh.GroupBox)
        filters_layout = QVBoxLayout(filters_group)

        # First line: Room Type, Check-in, Check-out, and Filter Button
        first_line_layout = QHBoxLayout()
        first_line_layout.addWidget(QLabel("Room Type:"))
        self.room_filter = QComboBox()
        self.room_filter.addItem("All")
        self.room_filter.addItems(["Single", "Double", "Suite"])
        self.room_filter.setStyleSheet(StyleShesh.ComboBox)
        first_line_layout.addWidget(self.room_filter)

        first_line_layout.addWidget(QLabel("Check-in:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate())
        self.date_from.setStyleSheet(StyleShesh.DateEdit)
        first_line_layout.addWidget(self.date_from)


        first_line_layout.addWidget(QLabel("Check-out:"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate().addDays(3))
        self.date_to.setStyleSheet(StyleShesh.DateEdit)
        first_line_layout.addWidget(self.date_to)

        self.btn_filter = QPushButton("Show Reserved Rooms")
        self.btn_filter.setStyleSheet(StyleShesh.Button)
        first_line_layout.addWidget(self.btn_filter)

        filters_layout.addLayout(first_line_layout)

        # Second line: Search User and Search Button
        second_line_layout = QHBoxLayout()
        second_line_layout.addWidget(QLabel("Search User or Number:"))
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet(StyleShesh.Input)
        second_line_layout.addWidget(self.search_input)
        self.btn_search = QPushButton("Search")
        self.btn_search.setStyleSheet(StyleShesh.Button)
        second_line_layout.addWidget(self.btn_search)

        filters_layout.addLayout(second_line_layout)

        root.addWidget(filters_group)

        # Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Client Name", "Room Type", "Check-in", "Check-out", "Room Price"])
        self.table.setStyleSheet(StyleShesh.Table)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.table)
        self.table.verticalHeader().setVisible(False)

        # Signals
        self.btn_filter.clicked.connect(self.on_filter)
        self.btn_search.clicked.connect(self.on_search)

        # Initial load
        self.on_filter()

    def _make_card(self, title: str, value: str):
        frame = QFrame()
        frame.setStyleSheet(StyleShesh.Card)
        layout = QVBoxLayout(frame)
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        label_value = QLabel(value)
        label_value.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        label_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(label_value)
        return frame, label_value

    def on_filter(self):
        start = self.date_from.date().toString("yyyy-MM-dd")
        end = self.date_to.date().toString("yyyy-MM-dd")

        if self.date_from.date() > self.date_to.date():
            QMessageBox.warning(self, "Invalid range", "Start date must be before or equal to end date.")
            return

        room = self.room_filter.currentText()
        rows = fetch_reservations(self.conn, start, end, room)
        show_table(self.table, rows)

        summary = calculate_summary(self.conn, rows)
        for key, value in summary.items():
            self.cards[key].setText(value)

    def on_search(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, "Empty Search", "Please enter a name or number to search.")
            return

        rows = search_user(self.conn, keyword)
        show_table(self.table, rows)

        summary = calculate_summary(self.conn, rows)
        for key, value in summary.items():
            self.cards[key].setText(value)