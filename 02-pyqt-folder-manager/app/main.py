import sys
from PyQt6.QtWidgets import QApplication

from layout import ProductivityAppMain
from functions import openFolder, newFolder

from database import Session
from models import Comment, Attachment, TaskDependency, MilestoneDependency, DeliverableDependency, QualityCriteria, AcceptanceCriteria, Project, Task, Deliverable, Milestone


if __name__ == "__main__":
    app = QApplication(sys.argv)
    session = Session()
    window = ProductivityAppMain(openFolder, newFolder, session)
    window.showMaximized()
    window.show()
    sys.exit(app.exec())
