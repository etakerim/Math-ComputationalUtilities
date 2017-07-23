import sys
import math
from collections import OrderedDict
from PySide import QtCore
from PySide import QtGui


class SigReDraw(QtCore.QObject):
    redraw = QtCore.Signal()


class Sinusoid:
    def __init__(self):
        super().__init__()
        self.sig = SigReDraw()
        self.settings = [self.__panelpos(), self.__panelcustom()]

    def sine_curve(self, x):
        return self.amp() * math.sin(self.period() * x + self.phaze())

    def draw(self, canvas):
        obj = QtGui.QPainterPath()
        y = self.sine_curve(0)
        start = canvas.cart2screen(self.x(), y + self.y())
        obj.moveTo(start[0], start[1])

        for x in range(0, int(self.cntperiod() * math.degrees(self.period()))):
            x = math.radians(x)
            y = self.sine_curve(x)
            surad = canvas.cart2screen(x + self.x(), y + self.y())
            obj.lineTo(surad[0], surad[1])

        return obj

    def __panelpos(self):
        coor = QtGui.QGroupBox('Súradnice')
        poslayout = QtGui.QGridLayout()

        xsetting = NumericSettings('X', -1000, 1000, ' px')
        ysetting = NumericSettings('Y', -1000, 1000, ' px')
        coor.setLayout(poslayout)

        xsetting.addtoGridLayout(poslayout, 0)
        ysetting.addtoGridLayout(poslayout, 1)

        xsetting.valuechanged.connect(self.sig.redraw)
        ysetting.valuechanged.connect(self.sig.redraw)

        self.x = lambda: xsetting.value()
        self.y = lambda: ysetting.value()

        return coor

    def __panelcustom(self):
        setting = QtGui.QGroupBox('Vlastnosti')
        sinlayout = QtGui.QGridLayout()

        slid_sinamp = NumericSettings('Amplitúda', 0, 600, ' px')
        slid_period = NumericSettings('Perióda', 0, 660, ' °')
        slid_phaze = NumericSettings('Fáza',  -360, 360, ' °')
        slid_periodlen = NumericSettings('Periód', 0, 20, 'x')
        setting.setLayout(sinlayout)

        slid_sinamp.addtoGridLayout(sinlayout, 0)
        slid_period.addtoGridLayout(sinlayout, 1)
        slid_phaze.addtoGridLayout(sinlayout, 2)
        slid_periodlen.addtoGridLayout(sinlayout, 3)

        slid_sinamp.valuechanged.connect(self.sig.redraw)
        slid_period.valuechanged.connect(self.sig.redraw)
        slid_phaze.valuechanged.connect(self.sig.redraw)
        slid_periodlen.valuechanged.connect(self.sig.redraw)

        self.amp = lambda: slid_sinamp.value()
        self.period = lambda: math.radians(slid_period.value())
        self.phaze = lambda: math.radians(slid_phaze.value())
        self.cntperiod = lambda: slid_periodlen.value()

        return setting


class CoordinateGrid:
    def draw(self, canvas):
        grid = QtGui.QPainterPath()
        w, h = canvas.dim
        origin = canvas.cart2screen(0, 0, w, h)
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
        self.isgridactive = False
        self.ggrid = CoordinateGrid()
        self.graphobj = None

        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)

    @property
    def dim(self):
        return (self.size().width(), self.size().height())

    def cart2screen(self, x, y):
        wscreen, hscreen = self.dim
        return (x + wscreen // 2, -y + hscreen // 2)

    def screen2cart(self, x, y):
        wscreen, hscreen = self.dim
        return (x - wscreen // 2, -y + hscreen // 2)

    def grid_activate(self):
        self.isgridactive = not self.isgridactive
        self.update()

    def paintEvent(self, event):
        w, h = self.dim
        p = QtGui.QPainter()

        p.begin(self)
        # p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.fillRect(event.rect(), QtGui.QColor(QtCore.Qt.white))

        if self.isgridactive:
            p.setPen(QtGui.QColor(110, 110, 110))
            p.drawPath(self.ggrid.draw(self))

        if self.graphobj:
            p.setPen(QtGui.QColor(0, 0, 255))
            p.drawPath(self.graphobj.draw(self))
        p.end()


class NumericSettings(QtCore.QObject):
    valuechanged = QtCore.Signal()

    def __init__(self, name, minimum, maximum,
                 unit='', step=1, default=None):
        super().__init__()
        self.name = QtGui.QLabel(name)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.valuebox = QtGui.QDoubleSpinBox()
        self.dpislid = step ** -1
        if not default:
            default = (minimum + maximum) // 2

        self.valuebox.setRange(minimum, maximum)
        self.valuebox.setSingleStep(step)
        self.valuebox.setDecimals(math.ceil(math.log10(self.dpislid)))
        self.valuebox.setSuffix(unit)
        self.slider.setRange(minimum, maximum * self.dpislid)

        self.slider.valueChanged.connect(self.valuechanged)
        self.valuebox.valueChanged.connect(self.valuechanged)
        self.slider.valueChanged.connect(self.valuesync)
        self.valuebox.valueChanged.connect(self.slidersync)
        self.slider.setValue(default)

    def addtoGridLayout(self, gridl, row):
        if isinstance(gridl, QtGui.QGridLayout):
            gridl.addWidget(self.name, row, 0)
            gridl.addWidget(self.slider, row, 1)
            gridl.addWidget(self.valuebox, row, 2)

    def slidersync(self):
        self.slider.setValue(self.valuebox.value() * self.dpislid)

    def valuesync(self):
        self.valuebox.setValue(self.slider.value() / self.dpislid)

    def value(self):
        return self.valuebox.value()


class MathShapener(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.MSHAPES = OrderedDict([
               ('--- Vyber útvar --- ', None),
               ('Sínusoida', Sinusoid()),
               ('Lissajousova krivka', None),
               ('Vektor', None),
               ('Kruh', None),
               ('Ruža', None),
               ('Kochova krivka', None),
               ('Kochova vločka', None),
               ('Serpinského koberec', None),
               ('Fraktálový strom', None),
               ('Mandelbrotova množina', None),
               ('L-system (Korytnačka)', None)
               ])

        self.mainlayout = QtGui.QHBoxLayout()

        self.leftlayout = QtGui.QVBoxLayout()
        self.leftlayout.addLayout(self.shape_select())
        self.canvas = Canvas()
        self.leftlayout.addWidget(self.canvas)

        # Udalosti
        self.gridsel.stateChanged.connect(self.canvas.grid_activate)
        self.shapesel.currentIndexChanged.connect(self.shape_change)

        self.rightlayout = QtGui.QVBoxLayout()
        self.rightlayout.setAlignment(QtCore.Qt.AlignTop)
        self.shape_change()

        self.rightlayout.addWidget(self.animation_setings())
        self.savebtn = QtGui.QPushButton('Uložiť obrázok')
        self.rightlayout.addWidget(self.savebtn)

        self.mainlayout.addLayout(self.leftlayout, 6)
        self.mainlayout.addLayout(self.rightlayout, 2)
        self.setLayout(self.mainlayout)

    def display_interval(self):
        val = self.slidinterval.value()
        self.intlabel.setText('Interval: {} ms'.format(val))

    def animation_setings(self):
        animgroup = QtGui.QGroupBox('Animácia')
        animlayout = QtGui.QFormLayout()

        self.intlabel = QtGui.QLabel()
        self.slidinterval = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slidinterval.setRange(10, 800)
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

    def shape_change(self):
        activeitm = self.MSHAPES[self.shapesel.currentText()]

        # Change drawn object
        olditm = self.canvas.graphobj
        self.canvas.graphobj = activeitm

        # Setup signals between Canvas() <--> DrawnObj()
        # Change Settings layout self <--> DrawnObj()
        if olditm:
            olditm.sig.redraw.disconnect()
            # Removing from beginning shifts items so go backwards
            for i in reversed(range(self.rightlayout.count())):
                self.rightlayout.takeAt(i).widget().setParent(None)

        if activeitm:
            activeitm.sig.redraw.connect(self.canvas.update)
            for setting in activeitm.settings:
                self.rightlayout.addWidget(setting)
        self.canvas.update()

    def shape_select(self):
        topmenu = QtGui.QHBoxLayout()

        self.shapesel = QtGui.QComboBox()
        self.shapesel.addItems([x for x in self.MSHAPES.keys()])
        self.gridsel = QtGui.QCheckBox('Mriežka')
        self.arealab = QtGui.QLabel('Plocha: ')
        self.circumlab = QtGui.QLabel('Obvod: ')

        topmenu.addWidget(self.shapesel, 5)
        topmenu.addWidget(self.arealab, 2)
        topmenu.addWidget(self.circumlab, 2)
        topmenu.addWidget(self.gridsel, 2)
        return topmenu


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
    window = AppWindow('Mathematical Shape Sharpener', (640, 480))
    app.exec_()
