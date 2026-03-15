import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
                            QRadioButton, QCheckBox, QComboBox, QListWidget, QTableWidget, QTableWidgetItem,
                            QSlider, QProgressBar, QDial, QDateEdit, QDateTimeEdit, QTimeEdit, QDialog, QScrollArea,
                            QHeaderView)
from PyQt6.QtCore import Qt, QDate, QDateTime, QTime

class CustomScrollArea(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        # Create a widget for the scroll area's viewport
        viewport_widget = QWidget()
        viewport_layout = QVBoxLayout()
        viewport_widget.setLayout(viewport_layout)

        for i in range(100):
            viewport_layout.addWidget(QLabel(f"Label {i}"))

        # Set the viewport widget
        scroll_area.setWidget(viewport_widget)

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("This is a dialog. ")
        layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

# This will create the dialog and make it modal
def showDialog():
    dialog = CustomDialog()
    dialog.exec()

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('PyQt6 Widgets')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # QLabel
        label = QLabel("This is a label.")
        layout.addWidget(label)

        # QLineEdit
        line_edit = QLineEdit()
        layout.addWidget(line_edit)

        # QTextEdit
        text_edit = QTextEdit()
        layout.addWidget(text_edit)

        # QPushButton
        button = QPushButton("This is a button.")
        layout.addWidget(button)

        # QPushButton with a callback
        button = QPushButton("This is a button with a callback.")
        button.clicked.connect(showDialog)
        layout.addWidget(button)

        # QRadioButton
        radio_button = QRadioButton("This is a radio button.")
        layout.addWidget(radio_button)

        # QCheckBox
        check_box = QCheckBox("This is a checkbox.")
        layout.addWidget(check_box)

        # QComboBox
        combo_box = QComboBox()
        combo_box.addItem("Choice 1")
        combo_box.addItem("Choice 2")
        layout.addWidget(combo_box)

        # QListWidget
        list_widget = QListWidget()
        list_widget.addItem("Item 1")
        list_widget.addItem("Item 2")
        layout.addWidget(list_widget)

        # QTableWidget
        table_widget = QTableWidget(2, 2)  # 2 rows, 2 columns
        table_widget.setHorizontalHeaderLabels(["Header 1", "Header 2"])
        table_widget.setVerticalHeaderLabels(["Row 1", "Row 2"])
        table_widget.setItem(0, 0, QTableWidgetItem("Item (1,1)"))
        table_widget.setItem(0, 1, QTableWidgetItem("Item (1,2)"))
        table_widget.setItem(1, 0, QTableWidgetItem("Item (2,1)"))
        table_widget.setItem(1, 1, QTableWidgetItem("Item (2,2)"))
        layout.addWidget(table_widget)
        
        # QSlider
        slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(slider)

        # QProgressBar
        progress_bar = QProgressBar()
        layout.addWidget(progress_bar)

        # QDial
        dial = QDial()
        layout.addWidget(dial)

        # QDateEdit, QDateTimeEdit, QTimeEdit
        date_edit = QDateEdit(QDate.currentDate())
        layout.addWidget(date_edit)
        datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        layout.addWidget(datetime_edit)
        time_edit = QTimeEdit(QTime.currentTime())
        layout.addWidget(time_edit)

        # QScrollArea
        scroll_area = CustomScrollArea()
        layout.addWidget(scroll_area)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
