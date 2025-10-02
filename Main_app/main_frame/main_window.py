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

        # Central container
        container = QWidget()
        layout = QHBoxLayout(container)
        self.setCentralWidget(container)

        # Main area (stack of pages)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Map feature names to widgets
        self.features = {}

        # Menu bar: Features menu (upper-left dropdown)
        menu_bar = self.menuBar()
        self.features_menu = menu_bar.addMenu("Features")

        # Keep a mapping action -> index
        self._menu_actions = {}

    def add_feature(self, name: str, factory):
        """
        Create the widget from factory(),
        add it to the stacked widget,
        and add a QAction to the Features dropdown menu.
        """
        widget = factory()
        idx = self.stack.addWidget(widget)
        self.features[name] = widget

        # Add to Features menu as a QAction
        action = QAction(name, self)
        action.triggered.connect(lambda checked=False, i=idx: self.stack.setCurrentIndex(i))
        self.features_menu.addAction(action)
        self._menu_actions[name] = action

    def show_feature(self, name: str):
        """Switch to a feature by name."""
        widget = self.features.get(name)
        if widget is None:
            return
        self.stack.setCurrentWidget(widget)
