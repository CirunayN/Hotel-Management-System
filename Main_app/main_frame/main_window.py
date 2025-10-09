from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget, QGroupBox,
)
from PyQt6.QtGui import QAction

from Main_app.core.stylesheet import StyleShesh


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel Reservation and Services")

        container = QWidget()
        layout = QHBoxLayout(container)
        self.setCentralWidget(container)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.menu = {}

        menu_bar = self.menuBar()
        self.features_menu = menu_bar.addMenu("Menu")

        box = QGroupBox()
        box.setStyleSheet(StyleShesh.GroupBox)
        self.features_menu.setStyleSheet(StyleShesh.Menu)

        self._menu_actions = {}

    def add_feature(self, name: str, factory):
        widget = factory()
        idx = self.stack.addWidget(widget)
        self.menu[name] = widget

        action = QAction(name, self)
        action.triggered.connect(lambda checked=False, i=idx: self.stack.setCurrentIndex(i))
        self.features_menu.addAction(action)
        self._menu_actions[name] = action

