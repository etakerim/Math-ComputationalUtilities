import sys
from PySide import QtCore
from PySide import QtGui


class Canvas(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        #self.drawRect(QRect(0, 0, 100, 100))
        pass 


class MathShapener(QtGui.QWidget):
    # Spraviť zoznam slovníkov a predávať len slovníkové pohľady
    MSHAPES = ['Sínus', 'Kosínus', 'Lissajousova krivka', 
                'Vektor', 'Kruh', 'Ruža', 'Kochova krivka', 
                'Kochova vločka', 'Serpinského koberec', 
                'Fraktálový strom', 'Mandelbrotova množina', 
                'L-system (Korytnačka)']

    def __init__(self):
        super().__init__()
        self.mainlayout = QtGui.QHBoxLayout()

        self.leftlayout = QtGui.QVBoxLayout()
        self.leftlayout.addLayout(self.shape_select())
        self.canvas = Canvas()
        self.leftlayout.addWidget(self.canvas)
        
        self.rightlayout = QtGui.QVBoxLayout()
        self.rightlayout.addWidget(self.xy_setting())
        self.rightlayout.addWidget(self.animation_setings())

        self.mainlayout.addLayout(self.leftlayout, 6)
        self.mainlayout.addLayout(self.rightlayout, 2)
        self.setLayout(self.mainlayout)

    def xy_setting(self):
        coor = QtGui.QGroupBox('Súradnice')
        self.posinfo_layout = QtGui.QFormLayout()
        
        xlabel = QtGui.QLabel('X: ')
        self.xdata = QtGui.QSpinBox()
        self.xdata.setRange(0, 600)
        ylabel = QtGui.QLabel('Y: ')
        self.ydata = QtGui.QSpinBox()
        self.ydata.setRange(0, 600)

        self.posinfo_layout.addRow(xlabel, self.xdata)
        self.posinfo_layout.addRow(ylabel, self.ydata)
        coor.setLayout(self.posinfo_layout)
        return coor

    def display_interval(self):
        val = self.slidinterval.value()
        self.intlabel.setText('Interval: {} ms'.format(val))

    def animation_setings(self):
        animgroup = QtGui.QGroupBox('Animácia')
        animlayout = QtGui.QFormLayout()
        
        self.intlabel = QtGui.QLabel()
        self.slidinterval = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slidinterval.setMinimum(10)
        self.slidinterval.setMaximum(500)
        self.slidinterval.setTickInterval(500 // 10)
        self.slidinterval.valueChanged.connect(self.display_interval)
        self.slidinterval.setValue(100)
        self.animplay = QtGui.QPushButton('Play/Stop')
        self.animpause = QtGui.QPushButton('Pauza')
        
        animlayout.addRow(self.intlabel)
        animlayout.addRow(self.slidinterval)
        ctrl_layout = QtGui.QHBoxLayout()
        ctrl_layout.addWidget(self.animplay)
        ctrl_layout.addWidget(self.animpause)
        animlayout.addRow(ctrl_layout)
        animgroup.setLayout(animlayout)

        return animgroup

    def shape_select(self):
        topmenu = QtGui.QHBoxLayout()
        
        self.shapesel = QtGui.QComboBox()
        self.shapesel.addItems(self.MSHAPES)
        self.isgridactive = QtGui.QCheckBox('Mriežka')
        self.savebtn = QtGui.QPushButton('Uložiť')
        
        topmenu.addWidget(self.shapesel, 5)
        topmenu.addWidget(self.savebtn, 2)
        topmenu.addWidget(self.isgridactive, 2)
        return topmenu


    def actions_global(self):
        # self.shapesel.activated('') = #func add widgets + their signals
        pass


class AppWindow(QtGui.QMainWindow):
    def __init__(self, title, min_size):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(*min_size)
        self.app = MathShapener()
        self.setCentralWidget(self.app)
        self.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = AppWindow('Mathematical Shape Sharpener', (600, 400))
    app.exec_()
