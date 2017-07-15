import sys
from PySide.QtCore import Qt, QTimer
from PySide.QtGui import (QApplication, QHBoxLayout, QVBoxLayout, QFormLayout,
                          QWidget, QMainWindow, QLabel, QPainter,
                          QPushButton, QPalette, QComboBox, QIcon, QPixmap,
                          QCheckBox, QSpinBox, QGroupBox, QSplitter)


class Canvas(QWidget):
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
        self.isgridactive = QCheckBox('Mriežka')
        self.topmenu.addWidget(self.shapesel, 4)
        self.topmenu.addWidget(self.isgridactive, 2)

        self.canvas = Canvas()
        self.leftlayout.addLayout(self.topmenu)
        self.leftlayout.addWidget(self.canvas)

        self.rightlayout = QVBoxLayout()
        self.coordgroup = QGroupBox('Súradnice')
        self.posinfo_layout = QFormLayout()
        self.xlabel = QLabel('X: ')
        self.xdata = QSpinBox()
        self.xdata.setRange(0, 600)
        self.ylabel = QLabel('Y: ')
        self.ydata = QSpinBox()
        self.ydata.setRange(0, 600)
        self.posinfo_layout.addRow(self.xlabel, self.xdata)
        self.posinfo_layout.addRow(self.ylabel, self.ydata)
        self.coordgroup.setLayout(self.posinfo_layout)
        self.rightlayout.addWidget(self.coordgroup)
        
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
