import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter, QTextEdit, QHBoxLayout, QSizePolicy

class CustomWidget(QWidget):
    def __init__(self, name):
        super().__init__()

        self.setWindowTitle('PyQt6 App')

        self.layout = QVBoxLayout()
        
        self.navigation = QTextEdit("Navigation")
        self.navigation.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        self.settings = QTextEdit("Settings")
        self.bottom = QTextEdit("Bottom")

        self.browse = QTextEdit("Browse")
        self.main = QTextEdit("Main")

        self.top_splitter = QSplitter()
        self.top_splitter.addWidget(self.settings)
        self.top_splitter.addWidget(self.main)
        self.top_splitter.setStretchFactor(0, 1)
        self.top_splitter.setStretchFactor(1, 2)

        self.middle_splitter = QSplitter()
        self.middle_splitter.addWidget(self.browse)
        self.middle_splitter.addWidget(self.main)
        self.middle_splitter.setStretchFactor(0, 1)
        self.middle_splitter.setStretchFactor(1, 2)

        self.bottom_splitter = QSplitter()
        self.bottom_splitter.addWidget(self.bottom)
        self.bottom_splitter.addWidget(self.main)
        self.bottom_splitter.setStretchFactor(0, 1)
        self.bottom_splitter.setStretchFactor(1, 2)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.navigation)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.top_splitter)
        self.right_layout.addWidget(self.middle_splitter)
        self.right_layout.addWidget(self.bottom_splitter)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addLayout(self.main_layout)
        self.horizontal_layout.addLayout(self.right_layout)

        self.setLayout(self.horizontal_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWidget("Main window")
    window.showMaximized()
    sys.exit(app.exec())
