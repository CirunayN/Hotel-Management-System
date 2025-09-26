import sys
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
    QTableWidgetItem, QSpinBox,
    QDateEdit, QComboBox,
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont, QColor,QIcon
import sqlite3
from .repo import ReservationItem
from Main_app.core.db import get_conn
from .func import MainFunc
from .data import Reservation


def build_view_reservation() -> QWidget:
    return ViewReservation()


class ViewReservation(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("View Reservation")

        # wiring: core -> repo -> service
        self.service = MainFunc(ReservationItem(get_conn()))

        # --- UI ---
        root = QVBoxLayout(self)

        form = QHBoxLayout()
        form_2 = QHBoxLayout()
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Name")
        # self.room_type = QLineEdit()
        # self.room_type.setPlaceholderText("Room Type")
        # self.layout.addWidget(QLabel("Room Type:"), 1, 0)
        self.room_type = QComboBox()
        self.room_type.addItems(["Single", "Double", "Suite"])
        # self.layout.addWidget(self.room_type, 1, 1)
        self.status = QLineEdit()
        self.status.setPlaceholderText("Status")
        self.price = QSpinBox()
        self.price.setRange(0, 10_000)
        self.check_in = QDateEdit()
        self.check_in.setCalendarPopup(True)
        self.check_in.setDate(QDate.currentDate())
        self.check_out = QDateEdit()
        self.check_out.setCalendarPopup(True)
        self.check_out.setDate(QDate.currentDate().addDays(1))
        self.btn_add = QPushButton("Add / Save")
        self.btn_clear = QPushButton("Clear")
        form.addWidget(QLabel("Name: "))
        form.addWidget(self.name_field)
        form.addWidget(QLabel("Room Type: "))
        form.addWidget(self.room_type)
        form.addWidget(QLabel("Check in: "))
        form.addWidget(self.check_in)
        form.addWidget(QLabel("Check_out: "))
        form.addWidget(self.check_out)
        form.addWidget(QLabel("Status: "))
        form.addWidget(self.status)
        form.addWidget(QLabel("Price: "))
        self.price.setFixedWidth(120)
        self.price.setMinimumWidth(150)
        form.addWidget(self.price)
        # form.addWidget(self.check_out, 1)
        form.addWidget(self.btn_add)
        form.addWidget(self.btn_clear)
        root.addLayout(form)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Room Type", "Check in", "Check_out", "Status","Price"])
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table)

        actions = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_delete = QPushButton("Delete Selected")
        actions.addWidget(self.btn_refresh)
        actions.addWidget(self.btn_delete)
        root.addLayout(actions)

        # state for editing
        self._editing_id: int | None = None

        # signals
        self.btn_add.clicked.connect(self.save)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_delete.clicked.connect(self.on_delete)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.refresh()

    def save(self):
        try:
            name = self.name_field.text().strip()
            # room_type = self.room_type.text()
            room_type = self.room_type.currentText()
            check_in = self.check_in.text()
            check_out = self.check_out.text()
            status = self.status.text().strip()
            price = self.price.value()


            if self._editing_id is None:
                # Create
                self.service.create(name, room_type, check_in, check_out,status,price)
            else:
                # Update
                data = Reservation(
                    id=self._editing_id,
                    name=name,
                    room_type=room_type,
                    check_in=check_in,
                    check_out=check_out,
                    status=status,
                    price=price
                )
                self.service.update(data)

            self.clear_form()
            self.refresh()

        except Exception as e:
            self.check_out.setPlaceholderText(f"Error: {e}")
            # self.check_out.setStyleSheet("QLineEdit { border: 1px solid #d33; }")

    def on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            return
        id_ = int(self.table.item(row, 0).text())
        self.service.delete(id_)
        if self._editing_id == id_:
            self.clear_form()
        self.refresh()



    def on_cell_double_clicked(self, row, _col):
        # Load row into form for editingv
        self._editing_id = int(self.table.item(row, 0).text())
        self.name_field.setText(self.table.item(row, 1).text())
        # self.room_type.setText(self.table.item(row, 2).text())
        self.room_type.setCurrentText(self.table.item(row, 2).text())
        self.check_in.setDate(self.table.item(row, 3).text())
        self.check_out.setDate(self.table.item(row, 4).text())
        # self.check_in.setDate(QDate.fromString(check_in_str, "yyyy-MM-dd"))
        # self.check_out.setDate(QDate.fromString(check_out_str, "yyyy-MM-dd"))
        self.status.setText(self.table.item(row, 5).text())
        self.price.setValue(self.table.item(row, 6).text())
        self.btn_add.setText("Save Changes")

    def clear_form(self):
        self._editing_id = None
        self.name_field.clear()
        # self.room_type.clear()
        self.room_type.setCurrentIndex(0)
        self.check_in.clear()
        self.check_out.clear()
        self.status.clear()
        self.price.clear()
        self.btn_add.setText("Add / Save")
        # self.check_out.setStyleSheet("")
        # self.check_out.setPlaceholderText("check_out (optional)")

    def refresh(self):
        items = self.service.list()
        self.table.setRowCount(len(items))
        for r, data in enumerate(items):
            self.table.setItem(r, 0, QTableWidgetItem(str(data.id)))
            self.table.setItem(r, 1, QTableWidgetItem(data.name))
            self.table.setItem(r, 2, QTableWidgetItem(data.room_type))
            self.table.setItem(r, 3, QTableWidgetItem(data.check_in))
            self.table.setItem(r, 4, QTableWidgetItem(data.check_out))
            self.table.setItem(r, 5, QTableWidgetItem(data.status))
            self.table.setItem(r, 6, QTableWidgetItem(str(data.price)))
            self.table.resizeColumnsToContents()











