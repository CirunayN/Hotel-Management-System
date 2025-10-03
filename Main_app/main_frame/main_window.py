# Main_app/main_frame/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel Management System")

        container = QWidget()
        layout = QHBoxLayout(container)
        self.setCentralWidget(container)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.menu = {}

        menu_bar = self.menuBar()
        self.features_menu = menu_bar.addMenu("Menu")

        self._menu_actions = {}

    def add_feature(self, name: str, factory):
        widget = factory()
        idx = self.stack.addWidget(widget)
        self.menu[name] = widget

        action = QAction(name, self)
        action.triggered.connect(lambda checked=False, i=idx: self.stack.setCurrentIndex(i))
        self.features_menu.addAction(action)
        self._menu_actions[name] = action

