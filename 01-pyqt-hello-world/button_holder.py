
from PyQt6.QtWidgets import QPushButton, QMainWindow

class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Button Holder App')
        button = QPushButton('Click This')

        self.setCentralWidget(button)
