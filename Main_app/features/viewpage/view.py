from cProfile import label

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


def build_main_page() -> QWidget:
    return ViewPage()


class ViewPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("View Page")


        # self.service = MainFunc(ReservationItem(get_conn()))
        font = QFont("Arial", 15)

        main = QVBoxLayout(self)
        self.main_label = (QLabel("Welcome To Hotel Transylvania"))
        self.main_label.setFont(QFont("Arial",24, QFont.Weight.Bold))
        main.addWidget(self.main_label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

