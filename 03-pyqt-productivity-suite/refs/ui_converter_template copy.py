from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton, QFileDialog
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        ui_file = 'productive_app_1.ui'
        
        # Load the UI file
        uic.loadUi(ui_file, self)

        # define widgets
        self.button = self.findChild(QPushButton, 'pushButton')

        # define signals
        self.button.clicked.connect(self.press_it)

        # show the window
        self.show()

    def press_it(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '',"All Files (*.*);; Python Files (*.py)")

        self.pixmap = QPixmap(fname)
        # Add pic map to label
        self.label.setPixmap(self.pixmap)

app = QApplication(sys.argv)
UIWindow = UI()
app.exec()