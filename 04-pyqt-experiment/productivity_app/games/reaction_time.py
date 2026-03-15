# game_widget.py
from PyQt6.QtCore import Qt, QRect, QTimer, QTime, pyqtSignal
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QBrush, QColor
import random


class ReactionTimeGameWidget(QWidget):
    game_over = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.square_side = 50
        self.max_squares = 10
        self.score = 0
        self.miss_penalty = 1
        self.time_penalty_factor = 1

        self.total_playtime = 60  # total playtime in seconds
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.check_playtime)
        self.play_timer.start(1000)  # check every second

        self.location = None
        self.start_time = QTime.currentTime()

    def showEvent(self, event):
        if not event.spontaneous():
            self.location = (random.randint(0, self.width() - self.square_side),
                             random.randint(0, self.height() - self.square_side))


    def check_playtime(self):
        if self.start_time.secsTo(QTime.currentTime()) >= self.total_playtime:
            print(f"Game ended. Total score: {self.score}")
            self.game_over.emit()


    def mousePressEvent(self, event):
        pos = event.pos()
        reaction_time = self.start_time.secsTo(QTime.currentTime())
        if reaction_time == 0:  # prevent division by zero error
            reaction_time = 1
        if self.location[0] <= pos.x() <= self.location[0] + self.square_side and \
                self.location[1] <= pos.y() <= self.location[1] + self.square_side:
            print(f"Hit! Reaction time: {reaction_time} seconds")
            score_increment = max(1, int(self.time_penalty_factor / reaction_time))
            self.score += score_increment
            print(f"Score: {self.score}")
            if self.score >= self.max_squares:
                print(f"Game ended. Total score: {self.score}")
                self.game_over.emit()
            self.location = (random.randint(0, self.width() - self.square_side),
                            random.randint(0, self.height() - self.square_side))
            self.start_time = QTime.currentTime()
        else:  # miss
            self.score -= self.miss_penalty
            print(f"Miss! Score: {self.score}")


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(255, 0, 0)))  # red
        painter.drawRect(QRect(self.location[0], self.location[1], self.square_side, self.square_side))
        self.update()