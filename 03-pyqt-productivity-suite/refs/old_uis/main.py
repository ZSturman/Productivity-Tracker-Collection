import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # Add a title
        self.setWindowTitle("Productivity App")

        # Set layout
        self.setLayout(qtw.QVBoxLayout())

        # Create a label
        main_label = qtw.QLabel("Productivity Stuff")
        main_label.setFont(qtg.QFont("Helvetica", 24))
        self.layout().addWidget(main_label)

        second_label = qtw.QLabel("Second Label")
        second_label.setFont(qtg.QFont("Helvetica", 18))
        self.layout().addWidget(second_label)

        third_label = qtw.QLabel("Third Label")
        third_label.setFont(qtg.QFont("Helvetica", 12))
        self.layout().addWidget(third_label)

        # Create an entry box
        text_entry = qtw.QLineEdit()
        text_entry.setObjectName("name_field")
        text_entry.setText("")
        self.layout().addWidget(text_entry)

        # Create a button
        my_button = qtw.QPushButton("Click Me!", clicked = lambda: press_it())
        self.layout().addWidget(my_button)


        # add a combo box
        my_combo = qtw.QComboBox(self)
        my_combo.addItem("First Item", 1)
        my_combo.addItem("Second Item", 2)
        my_combo.addItem("Third Item", 3)
        my_combo.addItem("Fourth Item", 4)
        my_combo.addItem("Fifth Item",  5)

        my_combo.move(50, 50)

        self.layout().addWidget(my_combo)

        my_text = qtw.QTextEdit(self, placeholderText = "Enter your text here", acceptRichText = False)
        self.layout().addWidget(my_text)

        form_layout = qtw.QFormLayout(self)
        new_label = qtw.QLabel("This is a new label for the form")
        form_layout.addRow(new_label)
        form_layout.addRow("Text Entry Box", qtw.QLineEdit())


        self.show()

        def press_it():
            main_label.setText(f"You pressed the button {text_entry.text()}!")
            self.resize(500, 500)
            text_entry.setText("")
            second_label.setText(f"{my_combo.currentText()} and {my_combo.currentIndex()} as well as {my_combo.currentData()}")
            third_label.setText(f"{my_text.toPlainText()}")

            new_button = qtw.QPushButton("New Button", clicked = lambda: press_it_new())

            self.layout().addWidget(new_button)

        def press_it_new():
            self.setLayout(form_layout)
            self.resize(300, 300)




app = qtw.QApplication([])
mw = MainWindow()

app.exec()