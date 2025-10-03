from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QGroupBox
)

from Main_app.core.db import get_conn_to_reservastion
from Main_app.features.services.func import ServicesFunc

def build_services_page() -> QWidget:
    return ServicesPage()



class ServicesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = get_conn_to_reservastion()
        self.func = ServicesFunc(self.conn)
        self.func.create_tables()

        # --- Layouts ---
        layout = QVBoxLayout(self)

        # Service input form
        form_box = QGroupBox("Add Service")
        form_layout = QHBoxLayout(form_box)

        self.svc_name = QLineEdit()
        self.svc_name.setPlaceholderText("Service Name")

        self.svc_cat = QComboBox()
        self.svc_cat.addItems(["Laundry", "Food", "Cleaning", "Other"])

        self.svc_price = QSpinBox()
        self.svc_price.setMaximum(10000)

        add_btn = QPushButton("Add Service")
        add_btn.clicked.connect(self.add_service)

        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.svc_name)
        form_layout.addWidget(QLabel("Category:"))
        form_layout.addWidget(self.svc_cat)
        form_layout.addWidget(QLabel("Price:"))
        form_layout.addWidget(self.svc_price)
        form_layout.addWidget(add_btn)

        layout.addWidget(form_box)

        # Service table
        self.table_services = QTableWidget(0, 4)
        self.table_services.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price"])
        layout.addWidget(self.table_services)

        # Reservation selector + Service selector
        selector_box = QGroupBox("Assign Service to Reservation")
        selector_layout = QHBoxLayout(selector_box)

        self.reservation_select = QComboBox()
        self.service_select = QComboBox()
        self.qty = QSpinBox()
        self.qty.setValue(1)
        assign_btn = QPushButton("Assign")
        assign_btn.clicked.connect(self.assign_service)

        selector_layout.addWidget(QLabel("Reservation:"))
        selector_layout.addWidget(self.reservation_select)
        selector_layout.addWidget(QLabel("Service:"))
        selector_layout.addWidget(self.service_select)
        selector_layout.addWidget(QLabel("Qty:"))
        selector_layout.addWidget(self.qty)
        selector_layout.addWidget(assign_btn)

        layout.addWidget(selector_box)

        # Orders table
        self.table_orders = QTableWidget(0, 4)
        self.table_orders.setHorizontalHeaderLabels(["Reservation ID", "Client", "Services", "Total"])
        layout.addWidget(self.table_orders)




        # Initial refresh
        self.refresh_services()
        self.refresh_reservations()
        self.refresh_orders()

    # --- GUI handlers (call functions) ---
    def add_service(self):
        name = self.svc_name.text().strip()
        cat = self.svc_cat.currentText()
        price = int(self.svc_price.value())
        if not name:
            QMessageBox.warning(self, "Validation", "Service name is required")
            return
        else:
            self.func.add_service(name, cat, price)
            self.svc_name.clear()
            self.svc_price.setValue(0)
            self.refresh_services()

    def refresh_services(self):
        rows = self.func.list_services()
        self.table_services.setRowCount(len(rows))
        self.service_select.clear()
        for r, row in enumerate(rows):
            service_id, name, cat, price = row
            self.table_services.setItem(r, 0, QTableWidgetItem(str(service_id)))
            self.table_services.setItem(r, 1, QTableWidgetItem(name))
            self.table_services.setItem(r, 2, QTableWidgetItem(cat))
            self.table_services.setItem(r, 3, QTableWidgetItem(str(price)))
            self.service_select.addItem(f"{name} (₱{price})", service_id)



    def refresh_reservations(self):
        rows = self.func.list_reservations()
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
        self.func.assign_service(rid, sid, qty)
        self.refresh_orders()

    def refresh_orders(self):
        rows = self.func.list_orders()
        self.table_orders.setRowCount(len(rows))
        for r, row in enumerate(rows):
            rid, client, services, total = row
            self.table_orders.setItem(r, 0, QTableWidgetItem(str(rid)))
            self.table_orders.setItem(r, 1, QTableWidgetItem(client or "—"))
            self.table_orders.setItem(r, 2, QTableWidgetItem(services or "—"))
            self.table_orders.setItem(r, 3, QTableWidgetItem(str(total or 0)))


