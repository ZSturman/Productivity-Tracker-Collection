from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('File Dialog')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        open_button = QPushButton("Open file")
        open_button.clicked.connect(self.open_file)
        layout.addWidget(open_button)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;Text Files (*.txt)", options=QFileDialog.Option.ReadOnly)

        if file_name:
            with open(file_name, 'r') as file:
                self.text_edit.setText(file.read())

if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    ex.show()
    app.exec()
