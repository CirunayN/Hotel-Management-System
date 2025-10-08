# stylesheet.py
class StyleShesh:
    RussianViolet = "#231942"
    UltraViolet = "#5E548E"
    AfricanViolet = "#9F86C0"
    Lilac = "#BE95C4"
    PinkLavender = "#E0B1CB"

    # --- Main Background (for Dashboard) ---
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


    # --- Buttons ---
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

    # --- Summary Cards ---
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

    # --- Table (used for Dashboard) ---
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

    # --- Input Fields ---
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

    # --- GroupBox / Panel styling ---
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

    # --- Enhanced DateEdit Styling ---
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



