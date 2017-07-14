import sys
from PySide.QtCore import Qt, QTimer
from PySide.QtGui import (QApplication, QWidget, QMainWindow, QLabel,
                          QPushButton, QComboBox, QIcon, QPixmap, QVBoxLayout)


class MathShapener(QWidget):
    def __init__(self):
        super().__init__()
        # Create app graphics


class AppWindow(QMainWindow):
    def __init__(self, title, min_size):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(*min_size)
        self.app = MathShapener()
        self.setCentralWidget(self.app)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow('Mathematical Shape Sharpener', (600, 400))
    app.exec_()
