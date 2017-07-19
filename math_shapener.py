import sys
import math
from PySide import QtCore
from PySide import QtGui


def cart2screen(x, y, wscreen, hscreen):
    return (x + wscreen // 2, -y + hscreen // 2)

def screen2cart(x, y, wscreen, hscreen):
    return (x - wscreen // 2, -y + hscreen // 2)

# Pozn.: Dedenie z QPathPaintera spôsobuje anomálie->inštancuj
class CoordinateGrid:
    def draw(self, w, h):
        grid = QtGui.QPainterPath()
        origin = cart2screen(0, 0, w, h)
        detail = 50
        
        for x in range(origin[0] % detail, w, detail):
            grid.moveTo(x, 0)
            grid.lineTo(x, h)

        for y in range(origin[1] % detail, h, detail):
            grid.moveTo(0, y)
            grid.lineTo(w, y)
        return grid


class Canvas(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.isgridactive = True
        self.ggrid = CoordinateGrid()
        self.gobj = None

        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)

    @property
    def dim(self):
        return (self.size().width(), self.size().height())

    def paintEvent(self, event):
        w, h = self.dim
        p = QtGui.QPainter()
        
        p.begin(self)
        # p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.fillRect(event.rect(), QtGui.QColor(QtCore.Qt.white)) 
        
        if self.isgridactive:
            p.setPen(QtGui.QColor(110, 110, 110))
            p.drawPath(self.ggrid.draw(w, h))

        if self.gobj:
            p.drawPath(self.gobj.draw(w, h))
        p.end()


class NumericSettings(QtGui.QHBoxLayout):
    def __init__(self, minimum, maximum, 
                 unit=' ', func_valuser=lambda x: x):
        super().__init__()
        self.valuelab = QtGui.QLabel()
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.func_valuser = func_valuser
        self.unit = unit

        self.slider.setRange(minimum, maximum)
        self.slider.valueChanged.connect(self.value_show)
        self.slider.setValue((maximum + minimum) // 2)
        self.slider.valueChanged.emit(0)

        self.addWidget(self.slider, 7)
        self.addWidget(self.valuelab, 3)
        self.setAlignment(self.valuelab, QtCore.Qt.AlignRight)

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
        poslayout = QtGui.QFormLayout()
        
        xsetting = NumericSettings(0, 600, ' px')
        ysetting = NumericSettings(0, 600, ' px')

        poslayout.addRow(QtGui.QLabel('X'), xsetting)
        poslayout.addRow(QtGui.QLabel('Y'), ysetting)
        coor.setLayout(poslayout)
        return coor

    def sinus_settings(self):
        setting = QtGui.QGroupBox('Vlastnosti objektu')
        sinlayout = QtGui.QFormLayout()
        
        self.slid_sinamp = NumericSettings(0, 300, ' px')  
        self.slid_period = NumericSettings(-360, 360, ' °')
        self.slid_phaze  = NumericSettings(-360, 360, ' °')
        self.periodlen   = NumericSettings(0, 20)

        sinlayout.addRow(QtGui.QLabel('Amplitúda'), self.slid_sinamp)
        sinlayout.addRow(QtGui.QLabel('Perióda'), self.slid_period)
        sinlayout.addRow(QtGui.QLabel('Fáza'), self.slid_phaze)
        sinlayout.addRow(QtGui.QLabel('# Periód'), self.periodlen)
        setting.setLayout(sinlayout) 

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
