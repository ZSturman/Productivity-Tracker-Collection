import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget
from button_holder import ButtonHolder

app = QApplication(sys.argv)

window = ButtonHolder()
window.show()

app.exec()