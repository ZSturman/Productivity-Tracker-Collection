from PyQt6 import QtWidgets
from app.widgets import ProjectWidget, ViewProjectsWidget
from app.layout import MainWindow

def main():
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.showMaximized()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
