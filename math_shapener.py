import sys
from PySide import QtCore
from PySide import QtGui


class Canvas(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        w = self.size().width()
        h = self.size().height()
        p = QtGui.QPainter()

        p.begin(self)
        p.fillRect(0, 0, w, h, QtGui.QColor(QtCore.Qt.white)) 
        p.end()
        pass


class NumericSettings(QtGui.QHBoxLayout):
    def __init__(self, name, minimum, maximum, 
                 unit='', func_valuser=lambda x: x):
        super().__init__()
        self.namelab = QtGui.QLabel(name)
        self.valuelab = QtGui.QLabel()
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.func_valuser = func_valuser
        self.unit = unit

        self.slider.setRange(minimum, maximum)
        self.slider.valueChanged.connect(self.value_show)
        self.slider.setValue((maximum + minimum) // 2)

        self.addWidget(self.namelab)
        self.addWidget(self.slider)
        self.addWidget(self.valuelab)

    def value_show(self):
        self.valuelab.setText('{}{}'.format(self.value(), self.unit))

    def slot_datachange(self, func):
        self.slider.valueChanged.connect(func)

    def value(self):
        return self.func_valuser(self.slider.value())


class MathShapener(QtGui.QWidget):
    # Spraviť zoznam slovníkov a predávať len slovníkové pohľady
    MSHAPES = ['--- Vyber útvar --- ', 'Sínusoida', 'Lissajousova krivka', 
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
        self.rightlayout.setAlignment(QtCore.Qt.AlignTop)
        self.rightlayout.addWidget(self.xy_settings())
        self.rightlayout.addWidget(self.sinus_settings())
        self.rightlayout.addWidget(self.animation_setings())
        self.savebtn = QtGui.QPushButton('Uložiť')
        self.rightlayout.addWidget(self.savebtn)
        
        self.mainlayout.addLayout(self.leftlayout, 6)
        self.mainlayout.addLayout(self.rightlayout, 2)
        self.setLayout(self.mainlayout)

    def xy_settings(self):
        coor = QtGui.QGroupBox('Súradnice')
        posinfo_layout = QtGui.QVBoxLayout()
        
        xsetting = NumericSettings('X: ', 0, 600, ' px')
        ysetting = NumericSettings('Y: ', 0, 600, ' px')

        posinfo_layout.addLayout(xsetting)
        posinfo_layout.addLayout(ysetting)
        coor.setLayout(posinfo_layout)
        return coor

    def sinus_settings(self):
        setting = QtGui.QGroupBox('Vlastnosti objektu')
        sinus_layout = QtGui.QVBoxLayout()
        
        self.slid_sinamp = NumericSettings('Amplitúda: ', 0, 300, ' px')  
        self.slid_period = NumericSettings('Perióda  : ', -360, 360, ' °')
        self.slid_phaze  = NumericSettings('Fáza     : ', -360, 360, ' °')

        sinus_layout.addLayout(self.slid_sinamp)
        sinus_layout.addLayout(self.slid_period)
        sinus_layout.addLayout(self.slid_phaze)
        setting.setLayout(sinus_layout) 

        return setting

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
        self.slidinterval.valueChanged.connect(self.display_interval)
        self.slidinterval.setValue(500)
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
        self.arealab = QtGui.QLabel('Plocha: ') 
        self.circumlab = QtGui.QLabel('Obvod: ')
       
        topmenu.addWidget(self.shapesel, 5)
        topmenu.addWidget(self.arealab, 2)
        topmenu.addWidget(self.circumlab, 2)
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
