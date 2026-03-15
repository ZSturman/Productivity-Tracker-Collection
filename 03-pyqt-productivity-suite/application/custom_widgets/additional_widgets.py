from PyQt6.QtWidgets import QHBoxLayout, QCheckBox, QLabel, QWidget
from PyQt6.QtCore import Qt

class UpcomingListItem(QWidget):
    def __init__(self, item):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create the checkbox
        self.checkbox = QCheckBox(item['title'])
        self.checkbox.setChecked(item['completed'])

        # Create the labels
        self.tableLabel = QLabel(item['table'])
        self.dueDateLabel = QLabel(item['due_date'])

        # Add them to the layout
        self.layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.tableLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.dueDateLabel, alignment=Qt.AlignmentFlag.AlignRight)