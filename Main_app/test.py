from PyQt6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
import sys

class MenuExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeWidget Menu Example")
        self.setGeometry(200, 200, 300, 250)

        layout = QVBoxLayout()

        # Tree as menu
        tree = QTreeWidget()
        tree.setHeaderHidden(True)  # hide the header, looks cleaner
        tree.setColumnCount(1)      # only 1 column for menu

        # "File" menu
        file_menu = QTreeWidgetItem(tree, ["File"])
        QTreeWidgetItem(file_menu, ["Open"])
        QTreeWidgetItem(file_menu, ["Save"])
        QTreeWidgetItem(file_menu, ["Exit"])

        # "Edit" menu
        edit_menu = QTreeWidgetItem(tree, ["Edit"])
        QTreeWidgetItem(edit_menu, ["Undo"])
        QTreeWidgetItem(edit_menu, ["Redo"])
        QTreeWidgetItem(edit_menu, ["Preferences"])

        # "Help" menu
        help_menu = QTreeWidgetItem(tree, ["Help"])
        QTreeWidgetItem(help_menu, ["About"])
        QTreeWidgetItem(help_menu, ["Check for updates"])

        # Expand only the first menu by default
        tree.expandItem(file_menu)

        # Connect click signal
        tree.itemClicked.connect(self.on_item_clicked)

        layout.addWidget(tree)
        self.setLayout(layout)

    def on_item_clicked(self, item, column):
        if item.childCount() == 0:  # leaf (menu option)
            print(f"Selected: {item.text(column)}")


app = QApplication(sys.argv)
window = MenuExample()
window.show()
sys.exit(app.exec())
