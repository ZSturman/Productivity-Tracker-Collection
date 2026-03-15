from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton, QFileDialog
from PyQt6 import uic
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        ui_file = 'testui.ui'
        
        # Load the UI file
        uic.loadUi(ui_file, self)

        # define widgets

        # show the window
        self.show()

app = QApplication(sys.argv)
UIWindow = UI()
app.exec()