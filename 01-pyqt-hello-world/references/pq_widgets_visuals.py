import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt

app = QApplication([])

# Create a scene
scene = QGraphicsScene()

# Add an ellipse to the scene
ellipse = QGraphicsEllipseItem(0, 0, 80, 60)
ellipse.setBrush(QBrush(Qt.GlobalColor.green))
scene.addItem(ellipse)

# Create a view to visualize the scene
view = QGraphicsView(scene)

view.show()

sys.exit(app.exec())
