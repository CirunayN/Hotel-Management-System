from datetime import datetime

from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
    QTableWidgetItem, QDateEdit, QComboBox, QMessageBox, QHeaderView, QGroupBox,
)
from PyQt6.QtCore import QDate, Qt, QRegularExpression
from .repo import ReservationItem
from Main_app.core.db import get_conn_to_reservastion
from .func import MainFunc
from Main_app.core.data import Reservation
from ...core.stylesheet import StyleShesh


def build_view_reservation() -> QWidget:
    return ViewReservation()


class ViewReservation(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("View Reservation")

        form_box = QGroupBox("Reservation Form")
        form_box.setStyleSheet(StyleShesh.GroupBox)

        form_main_layout = QVBoxLayout(form_box)

        self.setStyleSheet(StyleShesh.Page)
        title_font = QFont("Arial", 18, QFont.Weight.Bold)

        self.title = QLabel("Reservation")
        self.title.setFont(title_font)
        self.title.setStyleSheet(StyleShesh.TitleBanner)
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.service = MainFunc(ReservationItem(get_conn_to_reservastion()))

        root = QVBoxLayout(self)
        font = QFont("Arial", 16)
        label_font = QFont("Arial", 14)

        # Add title to root layout
        root.addWidget(self.title)

        # Create form fields
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Name")
        self.name_field.setFont(font)
        self.name_field.setStyleSheet(StyleShesh.Input)

        self.number_field = QLineEdit()
        self.number_field.setFont(font)
        self.number_field.setPlaceholderText("Phone Number")
        self.number_field.setStyleSheet(StyleShesh.Input)

        self.room_type = QComboBox()
        self.room_type.setFont(font)
        self.room_type.setStyleSheet(StyleShesh.Input)
        self.room_type.addItems(["Single", "Double", "Suite"])
        self.room_type.setStyleSheet(StyleShesh.ComboBox)

        self.check_in = QDateEdit()
        self.check_in.setFont(font)
        self.check_in.setStyleSheet(StyleShesh.Input)
        self.check_in.setCalendarPopup(True)
        self.check_in.setDate(QDate.currentDate())
        self.check_in.setStyleSheet(StyleShesh.DateEdit)

        self.check_out = QDateEdit()
        self.check_out.setFont(font)
        self.check_out.setStyleSheet(StyleShesh.Input)
        self.check_out.setCalendarPopup(True)
        self.check_out.setDate(QDate.currentDate().addDays(1))
        self.check_out.setStyleSheet(StyleShesh.DateEdit)

        self.btn_add = QPushButton("Add / Save")
        self.btn_add.setFont(QFont("Arial", 14))
        self.btn_add.setStyleSheet(StyleShesh.Button)
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setFont(QFont("Arial", 14))
        self.btn_clear.setStyleSheet(StyleShesh.Button)

        #First row: Name and Phone Number
        first_row_layout = QHBoxLayout()

        self.name_label = QLabel("Name: ")
        self.name_label.setFont(label_font)
        self.name_field.setMaxLength(100)
        self.name_field.setValidator(QRegularExpressionValidator(QRegularExpression(r"^[A-Za-zÀ-ÿ\s'\-]{1,100}$")))
        first_row_layout.addWidget(self.name_label)
        first_row_layout.addWidget(self.name_field)

        self.number_label = QLabel("Phone Number: ")
        self.number_label.setFont(label_font)
        self.number_field.setValidator(QRegularExpressionValidator(QRegularExpression(r"\d{0,11}$")))
        first_row_layout.addWidget(self.number_label)
        first_row_layout.addWidget(self.number_field)

        #Second row: Room Type, Check-in, Check-out
        second_row_layout = QHBoxLayout()

        self.room_type_label = QLabel("Room Type: ")
        self.room_type_label.setFont(label_font)
        second_row_layout.addWidget(self.room_type_label)
        second_row_layout.addWidget(self.room_type)

        check_in_label = QLabel("Check in: ")
        check_in_label.setFont(label_font)
        second_row_layout.addWidget(check_in_label)
        second_row_layout.addWidget(self.check_in)

        check_out_label = QLabel("Check out: ")
        check_out_label.setFont(label_font)
        second_row_layout.addWidget(check_out_label)
        second_row_layout.addWidget(self.check_out)

        #Third row: Buttons
        button_row_layout = QHBoxLayout()
        button_row_layout.addWidget(self.btn_add)
        button_row_layout.addWidget(self.btn_clear)

        #Add all rows to the main form layout
        form_main_layout.addLayout(first_row_layout)
        form_main_layout.addLayout(second_row_layout)
        form_main_layout.addLayout(button_row_layout)

        #Add the group box to root layout
        root.addWidget(form_box)

        #Create and setup table
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Phone Number", "Room Type", "Check in", "Check out"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet(StyleShesh.Table)
        self.table.horizontalHeader().setStretchLastSection(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

        root.addWidget(self.table)

        #Action buttons
        actions = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.setStyleSheet(StyleShesh.Button)
        self.btn_delete = QPushButton("Delete Selected")
        self.btn_delete.setStyleSheet(StyleShesh.Button)
        actions.addWidget(self.btn_refresh)
        actions.addWidget(self.btn_delete)
        root.addLayout(actions)

        self._editing_id: int | None = None

        #Connect signals
        self.btn_add.clicked.connect(self.save)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_delete.clicked.connect(self.on_delete)
        self.table.cellClicked.connect(self.on_table_click)

        self.refresh()

    def on_table_click(self, row, _col):
        self._editing_id = int(self.table.item(row, 0).text())
        self.name_field.setText(self.table.item(row, 1).text())
        self.number_field.setText(self.table.item(row, 2).text())
        self.room_type.setCurrentText(self.table.item(row, 3).text())
        check_in_str = self.table.item(row, 4).text()
        check_out_str = self.table.item(row, 5).text()
        self.check_in.setDate(QDate.fromString(check_in_str, "yyyy-MM-dd"))
        self.check_out.setDate(QDate.fromString(check_out_str, "yyyy-MM-dd"))
        self.btn_add.setText("Save Changes")

    def save(self):
        try:
            name = self.name_field.text().strip()
            number = self.number_field.text().strip()
            room_type = self.room_type.currentText()
            check_in = self.check_in.date().toString("yyyy-MM-dd")
            check_out = self.check_out.date().toString("yyyy-MM-dd")

            #Validate name
            if not name and self._editing_id is None:
                QMessageBox.warning(self, "Validation Error", "Name is required.")
                return

            #Validate phone number
            if len(number) != 11:
                QMessageBox.warning(self, "Validation Error", "Phone number must be exactly 11 digits.")
                return

            #Validate date range
            if self.check_in.date() > self.check_out.date():
                QMessageBox.warning(self, "Invalid Date Range",
                                    "Check-in date must be before check-out date.")
                return

            room_base_price = {
                "Single": 1000,
                "Double": 1800,
                "Suite": 3000
            }
            date_format = "%Y-%m-%d"
            check_in_date = datetime.strptime(check_in, date_format)
            check_out_date = datetime.strptime(check_out, date_format)

            nights = (check_out_date - check_in_date).days

            if nights <= 0:
                QMessageBox.warning(self, "Invalid Date Range",
                                    "Check-out date must be after check-in date.")
                return

            base_price = room_base_price.get(room_type)
            total_price = base_price * nights

            if self._editing_id is None:
                self.service.create(name, number, room_type, check_in, check_out, total_price)
                QMessageBox.information(self, "Success", "Reservation created successfully!")
            else:
                data = Reservation(
                    id=self._editing_id,
                    name=name,
                    number=number,
                    room_type=room_type,
                    check_in=check_in,
                    check_out=check_out,
                    price=total_price
                )
                self.service.update(data)
                QMessageBox.information(self, "Success", "Reservation updated successfully!")

            self.clear_form()
            self.refresh()

        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error saving reservation")
            msg.setText(str(e))
            msg.exec()

    def on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a reservation to delete.")
            return

        #Get the reservation details for confirmation message
        reservation_id = int(self.table.item(row, 0).text())
        client_name = self.table.item(row, 1).text()
        room_type = self.table.item(row, 3).text()

        #Confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the reservation for:\n\n"
            f"Client: {client_name}\n"
            f"Room Type: {room_type}\n"
            f"Reservation ID: {reservation_id}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete(reservation_id)
            if self._editing_id == reservation_id:
                self.clear_form()
            self.refresh()
            QMessageBox.information(self, "Success", "Reservation deleted successfully!")

    def clear_form(self):
        self._editing_id = None
        self.name_field.clear()
        self.number_field.clear()
        self.room_type.setCurrentIndex(0)
        self.check_in.setDate(QDate.currentDate())
        self.check_out.setDate(QDate.currentDate().addDays(1))
        self.btn_add.setText("Add / Save")

    def refresh(self):
        items = self.service.list()
        self.table.setRowCount(len(items))
        for r, data in enumerate(items):
            self.table.setItem(r, 0, QTableWidgetItem(str(data.id)))
            self.table.setItem(r, 1, QTableWidgetItem(data.name))
            self.table.setItem(r, 2, QTableWidgetItem(str(data.number)))
            self.table.setItem(r, 3, QTableWidgetItem(data.room_type))
            self.table.setItem(r, 4, QTableWidgetItem(data.check_in))
            self.table.setItem(r, 5, QTableWidgetItem(data.check_out))