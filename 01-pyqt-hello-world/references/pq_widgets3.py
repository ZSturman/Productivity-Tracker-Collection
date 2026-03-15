from PyQt6.QtWidgets import QApplication, QSpinBox

app = QApplication([])
spin_box = QSpinBox()
spin_box.setRange(0, 100)  # Set the range of the spin box to be between 0 and 100.
spin_box.show()

from PyQt6.QtWidgets import QApplication, QDoubleSpinBox

app = QApplication([])
double_spin_box = QDoubleSpinBox()
double_spin_box.setRange(0.0, 100.0)  # Set the range to be between 0.0 and 100.0.
double_spin_box.show()

from PyQt6.QtWidgets import QApplication, QSlider
from PyQt6.QtCore import Qt

app = QApplication([])
slider = QSlider(Qt.Orientation.Horizontal)  # Create a horizontal slider.
slider.setRange(0, 100)  # Set the range to be between 0 and 100.
slider.show()

from PyQt6.QtWidgets import QApplication, QScrollBar

app = QApplication([])
scroll_bar = QScrollBar()
scroll_bar.setRange(0, 100)  # Set the range to be between 0 and 100.
scroll_bar.show()

from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction

app = QApplication([])
window = QMainWindow()

menu_bar = QMenuBar()
menu = QMenu("File")
action = QAction("Open")
menu.addAction(action)
menu_bar.addMenu(menu)
window.setMenuBar(menu_bar)

window.show()

from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QAction

app = QApplication([])
window = QMainWindow()

tool_bar = QToolBar()
action = QAction("Open")
tool_bar.addAction(action)
window.addToolBar(tool_bar)

window.show()

from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar

app = QApplication([])
window = QMainWindow()

status_bar = QStatusBar()
window.setStatusBar(status_bar)
status_bar.showMessage("Ready")

window.show()
