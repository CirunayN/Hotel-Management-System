# stylesheet.py
class StyleShesh:

    #Main color palette generated from: https://coolors.co/
    RussianViolet = "#231942"
    UltraViolet = "#5E548E"
    AfricanViolet = "#9F86C0"
    Lilac = "#BE95C4"
    PinkLavender = "#E0B1CB"





    Page = f"""
    QWidget#Dashboard Page {{
        background-color: {RussianViolet};
        color: white;
        font-family: 'Segoe UI';
    }}
    """

    TitleBanner = f"""
    QLabel {{
        background-color: {UltraViolet};
        color: white;
        border-radius: 10px;
        padding: 15px;
        font-weight: bold;
        qproperty-alignment: AlignCenter;
    }}
    """


    Menu = f"""
    QMenu {{
        background-color: white;
        border: 2px solid {Lilac};
        border-radius: 8px;
        padding: 5px;
    }}
    QMenu::item {{
        background-color: transparent;
        padding: 8px 15px;
        border-radius: 4px;
        color: {RussianViolet};
        font-weight: bold;
    }}
    QMenu::item:selected {{
        background-color: {PinkLavender};
        color: {RussianViolet};
    }}
    QMenu::item:pressed {{
        background-color: {Lilac};
        color: white;
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {Lilac};
        margin: 5px 10px;
    }}
    """



    Button = f"""
    QPushButton {{
        background-color: {UltraViolet};
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {AfricanViolet};
    }}
    QPushButton:pressed {{
        background-color: {Lilac};
    }}
    """


    Card = f"""
    QFrame {{
        background-color: {AfricanViolet};
        border-radius: 10px;
        padding: 10px;
        color: white;
    }}
    QLabel {{
        color: white;
    }}
    """

    # --- Optional Card Header ---
    CardHeader = f"""
    QLabel {{
        font-size: 12px;
        font-weight: bold;
        color: #E0B1CB;
        letter-spacing: 0.5px;
    }}
    """


    Table = f"""
    QTableWidget {{
        background-color: #ffffff;
        gridline-color: {PinkLavender};
        border-radius: 6px;
        font-size: 13px;
        color: #2e2e2e;
    }}
    QTableWidget::item {{
        padding: 6px;
    }}
    QTableWidget::item:hover {{
        background-color: {PinkLavender};
        color: #231942;
    }}
    QHeaderView::section {{
        background-color: {Lilac};
        color: #231942;
        font-weight: bold;
        padding: 6px;
        border: none;
        border-radius: 3px;
    }}
    QHeaderView::section:hover {{
        background-color: {AfricanViolet};
    }}
"""

    Input = f"""
    QLineEdit, QComboBox, QDateEdit {{
        background-color: #ffffff;
        border: 1px solid {Lilac};
        border-radius: 6px;
        padding: 4px 8px;
        color: #231942;
    }}
    QLineEdit:hover, QComboBox:hover, QDateEdit:hover {{
        border: 1px solid {AfricanViolet};
    }}
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus {{
        border: 2px solid {AfricanViolet};
        background-color: #F9F6FB;
    }}
    """

    GroupBox = f"""
    QSpinBox {{
        background-color: white;
        border: 2px solid {Lilac};
        border-radius: 6px;
        padding: 5px 10px;
        color: {RussianViolet};
        font-weight: bold;
        font-size: 14px;
    }}
    QSpinBox::up-button {{
        background-color: {UltraViolet};
        border: none;
        border-top-right-radius: 4px;
        width: 20px;
        height: 10px;
    }}
    QSpinBox::up-button:hover {{
        background-color: {AfricanViolet};
    }}
    QSpinBox::up-button:pressed {{
        background-color: {Lilac};
    }}
    QSpinBox::down-button {{
        background-color: {UltraViolet};
        border-bottom-right-radius: 4px;
        width: 20px;
        height: 10px;
    }}
    QSpinBox::down-button:hover {{
        background-color: {AfricanViolet};
    }}
    QSpinBox::down-button:pressed {{
        background-color: {Lilac};
    }}
    QSpinBox::up-arrow {{
        width: 8px;
        height: 8px;
        color: white;
    }}
    QSpinBox::down-arrow {{
        width: 8px;
        height: 8px;
        color: white;
    }}
"""



    ComboBox = f"""
    QComboBox {{
        background-color: white;
        border: 2px solid {Lilac};
        border-radius: 8px;
        padding: 8px 12px;
        color: {RussianViolet};
        font-size: 13px;
        min-height: 20px;
        min-width: 100px;
    }}
    QComboBox:hover {{
        border: 2px solid {AfricanViolet};
    }}
    QComboBox:focus {{
        border: 2px solid {AfricanViolet};
        background-color: #F9F6FB;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 25px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {UltraViolet};
        width: 0px;
        height: 0px;
    }}
    QComboBox QAbstractItemView {{
        background-color: white;
        border: 2px solid {Lilac};
        border-radius: 8px;
        padding: 5px;
        selection-background-color: {PinkLavender};
        selection-color: {RussianViolet};
        outline: none;
    }}
    QComboBox QAbstractItemView::item {{
        padding: 8px 12px;
        border-radius: 4px;
        color: {RussianViolet};
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: {PinkLavender};
        color: {RussianViolet};
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: {Lilac};
        color: white;
    }}
    """


    DateEdit = f"""
    QDateEdit {{
        background-color: white;
        border: 2px solid {Lilac};
        border-radius: 8px;
        padding: 8px 12px;
        color: {RussianViolet};
        font-size: 13px;
        min-height: 20px;
        min-width: 120px;
    }}
    QDateEdit:hover {{
        border: 2px solid {AfricanViolet};
    }}
    QDateEdit:focus {{
        border: 2px solid {AfricanViolet};
        background-color: #F9F6FB;
    }}
    QDateEdit::drop-down {{
        border: none;
        width: 25px;
    }}
    QDateEdit::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {UltraViolet};
        width: 0px;
        height: 0px;
    }}
    """
    SpinBox = f"""
        QSpinBox {{
            background-color: white;
            border: 2px solid {Lilac};
            border-radius: 6px;
            padding: 5px 10px;
            color: {RussianViolet};
            font-weight: bold;
            selection-background-color: {PinkLavender};
        }}
        QSpinBox:hover {{
            border-color: {AfricanViolet};
        }}
        QSpinBox:focus {{
            border-color: {UltraViolet};
        }}
        QSpinBox::up-button {{
            background-color: {UltraViolet};
            border: none;
            border-top-right-radius: 4px;
            width: 20px;
            height: 10px;
        }}
        QSpinBox::up-button:hover {{
            background-color: {AfricanViolet};
        }}
        QSpinBox::up-button:pressed {{
            background-color: {Lilac};
        }}
        QSpinBox::down-button {{
            background-color: {UltraViolet};
            border: none;
            border-bottom-right-radius: 4px;
            width: 20px;
            height: 10px;
        }}
        QSpinBox::down-button:hover {{
            background-color: {AfricanViolet};
        }}
        QSpinBox::down-button:pressed {{
            background-color: {Lilac};
        }}
        QSpinBox::up-arrow {{
            width: 8px;
            height: 8px;
            color: white;
        }}
        QSpinBox::down-arrow {{
            width: 8px;
            height: 8px;
            color: white;
        }}
    """

    MessageBox = f"""
    QMessageBox {{
        background-color: white;
        border: 2px solid {Lilac};
        border-radius: 12px;
        font-family: 'Segoe UI';
        padding: 15px;
    }}

    QMessageBox QLabel {{
        color: {RussianViolet};
        font-size: 14px;
        font-weight: normal;
        line-height: 1.4;
    }}

    QMessageBox QLabel#qt_msgbox_label {{
        padding: 10px;
    }}

    QMessageBox QPushButton {{
        background-color: {UltraViolet};
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        min-width: 90px;
        margin: 5px;
    }}

    QMessageBox QPushButton:hover {{
        background-color: {AfricanViolet};
    }}

    QMessageBox QPushButton:pressed {{
        background-color: {Lilac};
    }}

    QMessageBox QPushButton:focus {{
        outline: 2px solid {PinkLavender};
    }}

    /* Danger buttons (No/Cancel in confirmation dialogs) */
    QMessageBox QPushButton[text="No"],
    QMessageBox QPushButton[text="Cancel"] {{
        background-color: {Lilac};
    }}

    QMessageBox QPushButton[text="No"]:hover,
    QMessageBox QPushButton[text="Cancel"]:hover {{
        background-color: {RussianViolet};
    }}

    /* Different border colors based on message type */
    QMessageBox[windowTitle*="Confirm"] {{
        border: 2px solid {UltraViolet};
    }}

    QMessageBox[windowTitle*="Validation"],
    QMessageBox[windowTitle*="Error"] {{
        border: 2px solid #DC2626;
    }}

    QMessageBox[windowTitle*="Success"] {{
        border: 2px solid #059669;
    }}

    QMessageBox[windowTitle*="Warning"] {{
        border: 2px solid #D97706;
    }}
    """


