from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QListWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel Management System")

        #Central container
        container = QWidget()
        layout = QHBoxLayout(container)
        self.setCentralWidget(container)

        # Sidebar (list of features)



        self.sidebarL = QListWidget()
        self.sidebarL.setFixedWidth(100)
        self.sidebarL.setFixedHeight(300)
        layout.addWidget(self.sidebarL)
        # layout.addWidget(self.sidebarL)


        # self.sidebarR = QHBoxLayout
        self.sidebar_right = QWidget()
        layout.addWidget(self.sidebar_right, stretch=0)

        # Main area (stack of pages)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Map feature names to widgets
        self.features = {}

        # Handle sidebar selection
        self.sidebarL.currentRowChanged.connect(self.stack.setCurrentIndex)

    def add_feature(self, name: str, factory):
        # Create widget for feature

        widget = factory()
        self.features[name] = widget

        # Add to sidebar
        item = QListWidgetItem(name)
        self.sidebarL.addItem(item)

        # Add to stacked widget
        self.stack.addWidget(widget)
