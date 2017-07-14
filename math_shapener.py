import sys
from PySide.QtCore import Qt, QTimer
from PySide.QtGui import (QApplication, QHBoxLayout, QVBoxLayout, QFormLayout,
                          QWidget, QMainWindow, QLabel, QPainter,
                          QPushButton, QPalette, QComboBox, QIcon, QPixmap,
                          QVBoxLayout, QSpinBox)


class Renderer(QWidget):
    def __init__(self):
        super().__init__()
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

    def draw(self):
        pass # QPaintEvent

class MathShapener(QWidget):
    def __init__(self):
        super().__init__()
        self.mainlayout = QHBoxLayout()

        self.leftlayout = QVBoxLayout()
        self.topmenu = QHBoxLayout()
        self.shapesel = QComboBox()
        mshapes = ['Sínus', 'Kosínus', 'Lissajousova krivka', 
                   'Vektor', 'Kruh', 'Ruža', 'Kochova krivka', 
                   'Kochova vločka', 'Serpinského koberec', 
                   'Fraktálový strom', 'Mandelbrotova množina', 
                   'L-system (Korytnačka)']
        self.shapesel.addItems(mshapes)
        self.topmenu.addWidget(self.shapesel)

        self.canvas = Renderer()
        self.leftlayout.addLayout(self.topmenu)
        self.leftlayout.addWidget(self.canvas)

        self.rightlayout = QVBoxLayout()
        self.posinfo_layout = QFormLayout()
        self.xlabel = QLabel('X: ')
        self.xdata = QSpinBox()
        self.xdata.setRange(0, 600)
        self.ylabel = QLabel('Y: ')
        self.ydata = QSpinBox()
        self.ydata.setRange(0, 600)
        self.posinfo_layout.addWidget(self.xlabel)
        self.posinfo_layout.addWidget(self.xdata)
        self.posinfo_layout.addWidget(self.ylabel)
        self.posinfo_layout.addWidget(self.ydata)
        self.rightlayout.addLayout(self.posinfo_layout)

        # ADD Widgets and layouts HBOX -> VBox(Menu,..Canvas) ...,
        # VBOX(Ovladác)
        self.mainlayout.addLayout(self.leftlayout, 4)
        self.mainlayout.addLayout(self.rightlayout, 2)
        self.setLayout(self.mainlayout)


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
