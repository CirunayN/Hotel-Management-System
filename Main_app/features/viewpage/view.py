from PyQt6.QtWidgets import QWidget, QVBoxLayout


def build_main_page() -> QWidget:
    return ViewPage()


class ViewPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("View Page")


        # self.service = MainFunc(ReservationItem(get_conn()))


        root = QVBoxLayout(self)