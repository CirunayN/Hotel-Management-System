import sys
from PyQt6.QtWidgets import QApplication

from Main_app.core.stylesheet import StyleShesh
from Main_app.main_frame.main_window import MainWindow
from Main_app.features.reservation.view import build_view_reservation
from Main_app.features.dashboard.view import build_dashboard_page
from Main_app.features.services.view import build_services_page

def main():
    app = QApplication(sys.argv)
    win = MainWindow()

    win.add_feature("Dashboard", build_dashboard_page)
    win.add_feature("Reservation", build_view_reservation)
    win.add_feature("Services", build_services_page)
    win.resize(1200, 760)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
