import sys
from PyQt6 import QtWidgets, QtCore, QtGui


class NewProjectForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NewProjectForm, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("This is Form 1", self)
        self.layout.addWidget(self.label)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.lineEdit)


class NewTaskForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NewTaskForm, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("This is Form 2", self)
        self.layout.addWidget(self.label)

        self.spinBox = QtWidgets.QSpinBox(self)
        self.layout.addWidget(self.spinBox)


class NewItemDialog(QtWidgets.QDialog):
    def __init__(self, session, parent=None):
        super(NewItemDialog, self).__init__(parent)

        self.session = session

        self.layout = QtWidgets.QVBoxLayout(self)

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.addItems(["Form 1", "Form 2"])
        self.layout.addWidget(self.comboBox)

        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.layout.addWidget(self.stackedWidget)

        self.new_project_form = NewProjectForm(self)
        self.new_task_form = NewTaskForm(self)

        self.stackedWidget.addWidget(self.new_project_form)
        self.stackedWidget.addWidget(self.new_task_form)

        self.comboBox.currentIndexChanged.connect(self.stackedWidget.setCurrentIndex)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel, self)
        self.layout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
