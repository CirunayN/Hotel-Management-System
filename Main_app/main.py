import sys
from PyQt6.QtWidgets import QApplication
from Main_app.main_frame.main_window import MainWindow
from Main_app.features.reservation.view import build_view_reservation


def main():
    app = QApplication(sys.argv)

    # Optional: load app stylesheet
    # try:
    #     with open("app/core/styles.qss", "r", encoding="utf-8") as f:
    #         app.setStyleSheet(f.read())
    # except FileNotFoundError:
    #     pass

    win = MainWindow()
    # win.add_feature("Main Page")
    win.add_feature("Reservation", build_view_reservation)
    win.resize(900, 560)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
