from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QGroupBox, QHeaderView, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from Main_app.core.db import get_conn_to_reservastion
from Main_app.features.services.repo import ServicesFunc
from Main_app.core.stylesheet import StyleShesh


def build_services_page() -> QWidget:
    return ServicesPage()


class ServicesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(StyleShesh.Page)

        self.conn = get_conn_to_reservastion()
        self.func = ServicesFunc(self.conn)
        self.func.create_tables()

        # Main root layout
        root = QVBoxLayout(self)

        # Title with banner styling
        title_font = QFont("Arial", 18, QFont.Weight.Bold)
        self.title = QLabel("Services")
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setStyleSheet(StyleShesh.TitleBanner)
        root.addWidget(self.title)

        # Main content layout (horizontal)
        main_layout = QHBoxLayout()
        root.addLayout(main_layout)

        # LEFT SIDE
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 2)

        # --- Add Service Box ---
        form_box = QGroupBox("Add / Manage Services")
        form_box.setStyleSheet(StyleShesh.GroupBox)
        form_layout = QHBoxLayout(form_box)

        self.service_name = QLineEdit()
        self.service_name.setPlaceholderText("Service Name")
        self.service_name.setStyleSheet(StyleShesh.Input)

        self.service_category = QComboBox()
        self.service_category.addItems(["Laundry", "Food", "Cleaning", "Other"])
        self.service_category.setStyleSheet(StyleShesh.ComboBox)

        self.service_price = QSpinBox()
        self.service_price.setMaximum(999999)
        self.service_price.setStyleSheet(StyleShesh.GroupBox)

        add_btn = QPushButton("Add Service")
        add_btn.setStyleSheet(StyleShesh.Button)
        add_btn.clicked.connect(self.add_service)

        del_btn = QPushButton("Remove Selected Service")
        del_btn.setStyleSheet(StyleShesh.Button)
        del_btn.clicked.connect(self.remove_service)

        form_layout.addWidget(QLabel("Service:"))
        form_layout.addWidget(self.service_name)
        form_layout.addWidget(QLabel("Category:"))
        form_layout.addWidget(self.service_category)
        form_layout.addWidget(QLabel("Price:"))
        form_layout.addWidget(self.service_price)
        form_layout.addWidget(add_btn)
        form_layout.addWidget(del_btn)

        left_layout.addWidget(form_box)

        # --- Services Table ---
        self.service_table = QTableWidget(0, 4)
        self.service_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price"])
        self.service_table.setStyleSheet(StyleShesh.Table)
        self.service_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.service_table.verticalHeader().setVisible(False)
        header_table = self.service_table.horizontalHeader()
        header_table.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_table.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_table.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_table.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        left_layout.addWidget(self.service_table)

        # --- Assign Box ---
        selector_box = QGroupBox("Assign Service to Client")
        selector_box.setStyleSheet(StyleShesh.GroupBox)
        selector_layout = QHBoxLayout(selector_box)

        self.reservation_select = QComboBox()
        self.reservation_select.setStyleSheet(StyleShesh.ComboBox)

        self.service_select = QComboBox()
        self.service_select.setStyleSheet(StyleShesh.ComboBox)

        self.qty = QSpinBox()
        self.qty.setValue(1)
        self.qty.setStyleSheet(StyleShesh.GroupBox)

        assign_btn = QPushButton("Assign")
        assign_btn.setStyleSheet(StyleShesh.Button)
        assign_btn.clicked.connect(self.assign_service)

        selector_layout.addWidget(QLabel("Reservation:"))
        selector_layout.addWidget(self.reservation_select)
        selector_layout.addWidget(QLabel("Service:"))
        selector_layout.addWidget(self.service_select)
        selector_layout.addWidget(QLabel("Qty:"))
        selector_layout.addWidget(self.qty)
        selector_layout.addWidget(assign_btn)

        left_layout.addWidget(selector_box)

        # --- Orders Table ---
        self.order_table = QTableWidget(0, 4)
        self.order_table.setHorizontalHeaderLabels(["Reservation ID", "Client", "Services", "Total"])
        self.order_table.setStyleSheet(StyleShesh.Table)
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header = self.order_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        left_layout.addWidget(self.order_table)

        # Pay button
        pay_btn = QPushButton("Generate Receipt")
        pay_btn.setStyleSheet(StyleShesh.Button)
        pay_btn.clicked.connect(self.generate_receipt)
        left_layout.addWidget(pay_btn)

        # === RIGHT SIDE: Receipt Panel ===
        right_box = QGroupBox("Receipt")
        right_box.setStyleSheet(StyleShesh.GroupBox)
        right_layout = QVBoxLayout(right_box)

        self.receipt_display = QTextEdit()
        self.receipt_display.setReadOnly(True)
        self.receipt_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: white;
                border: 1px solid {StyleShesh.Lilac};
                border-radius: 6px;
                padding: 15px;
                font-family: 'Courier New';
                font-size: 13px;
                color: {StyleShesh.RussianViolet};
            }}
        """)
        right_layout.addWidget(self.receipt_display)

        main_layout.addWidget(right_box, 1)

        self.refresh_services()
        self.refresh_reservations()
        self.refresh_orders()

    #Add service
    def add_service(self):
        name = self.service_name.text().strip()
        cat = self.service_category.currentText()
        price = int(self.service_price.value())

        if not name:
            QMessageBox.warning(self, "Validation", "Service name is required.")
            return

        self.func.add_service(name, cat, price)
        self.service_name.clear()
        self.service_price.setValue(0)
        self.refresh_services()

    #Remove service
    def remove_service(self):
        selected = self.service_table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Selection", "Please select a service to remove.")
            return

        sid = int(self.service_table.item(selected, 0).text())
        name = self.service_table.item(selected, 1).text()

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the service '{name}'?\n"
            f"This will also remove it from any existing assigned orders.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.func.delete_service_and_orders(sid)
            self.refresh_services()
            self.refresh_orders()

    #Refresh tables
    def refresh_services(self):
        rows = self.func.list_services()
        self.service_table.setRowCount(len(rows))
        self.service_select.clear()
        for r, row in enumerate(rows):
            sid, name, cat, price = row
            self.service_table.setItem(r, 0, QTableWidgetItem(str(sid)))
            self.service_table.setItem(r, 1, QTableWidgetItem(name))
            self.service_table.setItem(r, 2, QTableWidgetItem(cat))
            self.service_table.setItem(r, 3, QTableWidgetItem(f"₱{price}"))
            self.service_select.addItem(f"{name} (₱{price})", sid)

    def refresh_reservations(self):
        rows = self.func.list_reservations()
        self.reservation_select.clear()
        for row in rows:
            rid, name, check_in, check_out = row
            self.reservation_select.addItem(f"ID: {rid} | Client Name: {name}", rid)

    def refresh_orders(self):
        rows = self.func.list_orders()
        self.order_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            rid, client, services, total = row
            self.order_table.setItem(r, 0, QTableWidgetItem(str(rid)))
            self.order_table.setItem(r, 1, QTableWidgetItem(client or "—"))
            self.order_table.setItem(r, 2, QTableWidgetItem(services or "—"))
            self.order_table.setItem(r, 3, QTableWidgetItem(f"₱{total or 0}"))

    #Assign service
    def assign_service(self):
        if self.reservation_select.count() == 0 or self.service_select.count() == 0:
            QMessageBox.warning(self, "Validation", "Select a reservation and service first.")
            return
        rid = int(self.reservation_select.currentData())
        sid = int(self.service_select.currentData())
        qty = int(self.qty.value())
        self.func.assign_service(rid, sid, qty)
        self.refresh_orders()

    #Generate receipt
    def generate_receipt(self):
        selected = self.order_table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Selection", "Please select an order first.")
            return

        rid = self.order_table.item(selected, 0).text()
        client = self.order_table.item(selected, 1).text()
        services = self.order_table.item(selected, 2).text()
        total = self.order_table.item(selected, 3).text()

        receipt_text = (
            f"🧾 HOTEL SERVICE RECEIPT\n"
            f"---------------------------\n"
            f"Reservation ID: {rid}\n"
            f"Client Name: {client}\n"
            f"Services Availed:\n{services}\n\n"
            f"Total Amount: {total}\n"
            f"---------------------------\n"
            f"Thank you for your payment!\n"
        )
        self.receipt_display.setText(receipt_text)

        #Remove after payment
        self.func.remove_order(int(rid))
        self.refresh_orders()