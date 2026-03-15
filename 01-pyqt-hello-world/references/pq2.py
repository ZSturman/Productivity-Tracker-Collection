import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit
from PyQt6.QtCore import Qt

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Streamlit Like App')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add a QLineEdit
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        # Add a Button
        button = QPushButton("Add folder")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)

        # Add a ListWidget
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.update_folder_list()

    def on_button_clicked(self):
        # Add a folder to the directory
        base_dir = "./"  # base directory where you want to create folders
        folder_name = self.line_edit.text()  # new folder name from QLineEdit
        new_folder_path = os.path.join(base_dir, folder_name)
        
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        
        self.update_folder_list()

    def update_folder_list(self):
        # Update the list widget with all folders in the base directory
        self.list_widget.clear()
        base_dir = "./"  # base directory where you are creating folders
        for folder_name in os.listdir(base_dir):
            if os.path.isdir(os.path.join(base_dir, folder_name)):
                self.list_widget.addItem(folder_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
