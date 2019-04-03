import sys

import decimal as dc

import numpy as np
import sympy as sp
from math import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker


app = QApplication(sys.argv)

PROGRAMME_NAME = "Graph builder"
PROGRAMME_ICON = QIcon("ProrgammeLogo.png")
PROGRAMME_ICON_ADRESS = "ProrgammeLogo.png"
TEXT_FONT = QFont("Times New Roman", 16)
MAX_PLOTS = 10
PROGRAMME_SLOGAN = "Тебе не понадобится глазомер!"
PROGRAMME_DESCRIBTION = '''  
Графики занимают определенное место место в нашей жизни.
Порой человек этого не замечает, но если вдуматься, то
в большинстве отраслей, графики являются одной из 
составляющей огромного проекта.
 
    Моя программа сможет быстро и точно построить график
любой сложности, что облегчает работу некоторым 
сотрудникам и сокращает время работы. Также данную 
программуможно использовать  студентам и школьникам
в качестве проверки некоторых заданий из курса математики.
'''
STARTWINDOW_BACKGROUND_COLOR = "#00bfff"
CREATOR_INFO = "Создано Домрачевым Иваном, 10 класс"
# PROGRAMME_COLOR = #6A5ACD
SCALE_MAX = 10000
SCALE_MIN = 0.01
MAX_PLOT_SYMBOLS = 25

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setMaximumSize(640, 480)
        self.setMinimumSize(640, 480)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        cp = QDesktopWidget().availableGeometry().center()
        self.frameGeometry().moveCenter(cp)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:"+STARTWINDOW_BACKGROUND_COLOR)

        self.startButton = QPushButton("Начать работу", self)
        self.aboutProgrammeButton = QPushButton("О программе", self)
        self.closeButton = QPushButton("Выход", self)
        self.programmeNameLabel = QLabel(PROGRAMME_NAME, self)
        self.programmeSloganLabel = QLabel(PROGRAMME_SLOGAN, self)

        self.startButton.setFont(QFont("Courier New", 10))
        self.aboutProgrammeButton.setFont(QFont("Courier New", 10))
        self.closeButton.setFont(QFont("Courier New", 10))
        self.programmeNameLabel.setFont(QFont("Comic Sans MS", 28))
        self.programmeSloganLabel.setFont(QFont("Courier New", 14))

        self.startButton.setStyleSheet("background-color:#ffffff")
        self.aboutProgrammeButton.setStyleSheet("background-color:#ffffff")
        self.closeButton.setStyleSheet("background-color:#ffffff")
        # self.programmeNameLabel.setStyleSheet("")
        # self.programmeSloganLabel.setStyleSheet("")

        self.startButton.clicked.connect(self.startButtonClicked)
        self.aboutProgrammeButton.clicked.connect(self.aboutProgrammeButtonClicked)
        self.closeButton.clicked.connect(QCoreApplication.instance().quit)

        self.startButton.setGeometry(self.width()*0.4, self.height()*0.65, self.width()*0.2, self.height()*0.05)
        self.aboutProgrammeButton.setGeometry(self.width()*0.4, self.height()*0.75, self.width()*0.2, self.height()*0.05)
        self.closeButton.setGeometry(self.width()*0.4, self.height()*0.85, self.width()*0.2, self.height()*0.05) #???????
        self.programmeNameLabel.setGeometry(self.width()*0.32, self.height()*0.05, self.width()*0.8, self.height()*0.2)
        self.programmeSloganLabel.setGeometry(self.width()*0.25, self.height()*0.2, self.width()*0.8, self.height()*0.15)

        self.show()

    def startButtonClicked(self):
        mainWindow.show()
        aboutProgrammeWindow.hide()
        self.close()

    def aboutProgrammeButtonClicked(self):
        aboutProgrammeWindow.show()

class AboutProgrammeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setMaximumSize(640, 480)
        self.setMinimumSize(640, 480)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        cp = QDesktopWidget().availableGeometry().center()
        self.frameGeometry().moveCenter(cp)

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setStyleSheet("background-color:#0bda51")

        self.infoTitle = QLabel(PROGRAMME_NAME, self)
        self.infoSubtitle = QLabel(PROGRAMME_SLOGAN, self)
        self.infoText = QLabel(PROGRAMME_DESCRIBTION, self)
        self.infoCreator = QLabel(CREATOR_INFO, self)
        self.closeButton = QPushButton("Выход", self)

        self.closeButton.setStyleSheet("background-color:#ffffff")

        self.logoImage = QPixmap(PROGRAMME_ICON_ADRESS)
        self.programmeLogo = QLabel(self)
        self.programmeLogo.setStyleSheet("background-color:#ffffff")
        self.programmeLogo.setPixmap(self.logoImage)
        self.programmeLogo.resize(self.logoImage.width(), self.logoImage.height())


        self.infoTitle.setFont(QFont("Comic Sans MC", 24))
        self.infoSubtitle.setFont(QFont("Courier New", 16))
        self.infoText.setFont(QFont("Courier New", 10))
        self.infoCreator.setFont(QFont("Courier New", 10))
        self.closeButton.setFont(QFont("Courier New", 10))

        self.infoCreator.setStyleSheet("color:#000080")

        self.closeButton.clicked.connect(self.hide)

        self.infoTitle.move(self.width()*0.05, self.height()*0.05)
        self.programmeLogo.move(self.width()*0.75, self.height()*0.05)
        self.infoSubtitle.move(self.width()*0.05, self.height()*0.2)
        self.infoText.move(self.width()*0.05, self.height()*0.4)
        self.infoCreator.move(self.width()*0.005, self.height()*0.965)
        self.closeButton.setGeometry(self.width()*0.792, self.height()*0.937, self.width()*0.2, self.height()*0.05)

class AxesEquation:
    def __init__(self, formula=None, equation = None, color="#000000"):
        self.equation = equation

        self.formula = sp.simplify(formula[formula.find('=')+1:])
        self.stringFormula = equation

        self.color = color
        self.isVisible = True

        self.xZeroPoints = sp.solveset(sp.Eq(self.formula, 0), x)
        self.yZeroPoints =  self.formula.subs(x, 0)

        self.points = list()

        self.derivatives = [sp.diff(self.formula), ]

    def changeColor(self, color):
        self.color = color

    def crossCut(self, axes1, axes2):
        xArgs = sp.solveset(sp.Eq(axes1.formula, axes2.formula), x)
        yArgs = {axes1.formula.subs(x, i) for i in xArgs}

    def addingPoints(self, xCoord = None, yCoord = None):
        if xCoord is None:
            yCoord = self.formula.subs(x, xCoord)
            self.points.insert({xCoord, yCoord})
        else:
            xCoord = sp.solveset(self.formula-yCoord)

            for i in xCoord:
                self.points.insert({i, yCoord})

    def addNewOrderDerivate(self):
        self.derivatives.append(sp.diff(self.derivatives[-1]))

    def countingRangeSpace(self):
        pass

    def funcExtremum(self):
        pass

class Signal(QObject):
    cleanLineEditSignal = pyqtSignal()
    plotAddedSignal = pyqtSignal(AxesEquation)
    plotVisibilityChangedSignal = pyqtSignal(tuple)
    plotColorChangedSignal = pyqtSignal(tuple)
    plotDeletedSignal = pyqtSignal(int)
    scaleChanged = pyqtSignal(bool)

class MainWindow(QMainWindow):
    signals = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowIcon(PROGRAMME_ICON)
        self.setWindowTitle(PROGRAMME_NAME)

        self.setMinimumSize(1024, 720)

        cp = QDesktopWidget().availableGeometry().center()
        self.frameGeometry().moveCenter(cp)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.plotCanvas = PlotCanvas(self)

        self.plotSettings = QWidget()
        self.plotSettingsLayout = QGridLayout()
        self.plotSettings.setLayout(self.plotSettingsLayout)

        self.lineEdit = QLineEdit()
        MainWindow.signals.cleanLineEditSignal.connect(self.clearLineEdit)

        self.yLabel = QLabel("y =")
        self.yLabel.setStyleSheet("color: white")
        self.yLabel.setAlignment(Qt.AlignRight)
        self.yLabel.setFont(TEXT_FONT)

        self.plotColorButton = PlotColorChoiceButton()

        self.buildButton = QPushButton()
        self.buildButton.setText("Нарисовать")
        self.buildButton.setFont(TEXT_FONT)
        self.buildButton.clicked.connect(self.buildButtonClicked)

        self.discardButton = QPushButton()
        self.discardButton.setText("Отмена")
        self.discardButton.setFont(TEXT_FONT)
        self.discardButton.clicked.connect(self.discardButtonClicked)

        self.plotList = QWidget()
        self.plotListLayout = QGridLayout()
        self.plotList.setLayout(self.plotListLayout)
        self.plotsBill = list()

        self.minusScaleButton = QPushButton()
        self.minusScaleButton.setMinimumSize(22, 22)
        self.minusScaleButton.setMaximumSize(22, 22)
        self.minusScaleButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.minusScaleButton.setIcon(QIcon("minus.png"))
        self.minusScaleButton.setFont(TEXT_FONT)

        self.minusScaleButton.clicked.connect(self.minusScaleButtonClicked)
        self.minusScaleButton.setAutoRepeat(True)
        self.minusScaleButton.setAutoRepeatDelay(200)

        self.scaleLabel = QLabel("Масштаб")
        self.scaleLabel.setFont(TEXT_FONT)
        self.scaleLabel.setAlignment(Qt.AlignCenter)

        self.plusScaleButton = QPushButton()
        self.plusScaleButton.setMinimumSize(22, 22)
        self.plusScaleButton.setMaximumSize(22, 22)
        self.plusScaleButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.plusScaleButton.setIcon(QIcon("plus.png"))
        self.plusScaleButton.setFont(TEXT_FONT)

        self.plusScaleButton.clicked.connect(self.plusScaleButtonClicked)
        self.plusScaleButton.setAutoRepeat(True)
        self.plusScaleButton.setAutoRepeatDelay(200)

        MainWindow.signals.plotAddedSignal.connect(self.plotAdded)

        MainWindow.signals.plotDeletedSignal.connect(self.plotDeleted)

        self.plotSettingsLayout.addWidget(self.lineEdit, 0, 1, 1, 8)
        self.plotSettingsLayout.addWidget(self.yLabel, 0, 0, 1, 1)
        self.plotSettingsLayout.addWidget(self.plotColorButton, 0, 9, 1, 1)
        self.plotSettingsLayout.addWidget(self.buildButton, 1, 0, 1, 5)
        self.plotSettingsLayout.addWidget(self.discardButton, 1, 5, 1, 5)

        self.plotSettingsLayout.addWidget(self.plotList, 2, 0, 9, 10)

        self.plotSettingsLayout.addWidget(self. minusScaleButton, 10, 2, 1, 1)
        self.plotSettingsLayout.addWidget(self. scaleLabel, 10, 3, 1, 4)
        self.plotSettingsLayout.addWidget(self. plusScaleButton, 10, 7, 1, 1)

        self.layout = QGridLayout(self.centralWidget)
        self.layout.addWidget(self.plotSettings, 0, 0, -1, 6)
        self.layout.addWidget(self.plotCanvas, 0, 6, -1, 14)
        self.setLayout(self.layout)

        # self.lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.menuBar = MenuBar()
        self.setMenuBar(self.menuBar)

        self.setStyleSheet('''
            QMainWindow{background-color:#3c3f41}

            QMenuBar{border-bottom-style: ridge; border-bottom-width: 1px;border-bottom-color:#1a1a1a; color:white}
            QMenuBar::item{background-color:#3c3f41}
            QMenuBar::item:hovered{background-color:#3c3f41}
            QMenuBar::item:pressed{background-color:#496DAB}
            QMenuBar:pressed{background-color:#3c3f41}

            QPushButton{background-color: white; color: black}
            QPushButton:hover{background-color:#aaaaaa}
            QPushButton:pressed{background-color:#aaaaaa}
            
            QLineEdit{background-color:white; border-style: solid; border-width:3px; border-color:white; border-radius: 9px;}"
            
            QPushButton#minusScaleButton, QPushButton#plusScaleButton{border-style: solid; border-width: 1px; border-radius: 11px; background-color: #3c3f41;border-color: #3c3f41}
        ''')
        self.minusScaleButton.setStyleSheet("border-style: solid; border-width: 1px; border-radius: 11px; background-color: #3c3f41;border-color: #3c3f41")
        self.plusScaleButton.setStyleSheet("border-style: solid; border-width: 1px; border-radius: 11px; background-color: #3c3f41;border-color: #3c3f41")
        self.scaleLabel.setStyleSheet("color: white; text-decoration: underline")

    def plotAdded(self, plot):
        newPlot = PlotListContainer(str(len(self.plotsBill)+1), plot.equation, plot.color)

        self.plotsBill.append(newPlot)
        self.redrawPlotList()

    def redrawPlotList(self):
        for i in reversed(range(self.plotListLayout.rowCount()-1)):
            widgetToRemove = self.plotListLayout.itemAtPosition(i, 0).widget()
            # remove it from the layout list
            self.plotListLayout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)



        for i in range(len(self.plotsBill)):
            self.plotListLayout.addWidget(self.plotsBill[i], i, 0, 1, 1)

        for i in range(len(self.plotsBill), MAX_PLOTS+1):
            self.plotListLayout.addWidget(QLabel(''), i, 0, 1, 1)

    def buildButtonClicked(self):
        if 0 < len(self.lineEdit.text()) <= MAX_PLOT_SYMBOLS:
            self.plotCanvas.addPlot("y="+self.lineEdit.text(), self.plotColorButton.currentColor)
        else:
            MainWindow.signals.cleanLineEditSignal.emit()

    def discardButtonClicked(self):
        MainWindow.signals.cleanLineEditSignal.emit()

    def clearLineEdit(self):
        self.lineEdit.clear()

    def plotDeleted(self, index):
        self.plotsBill.pop(index-1)

        for i in range(len(self.plotsBill)):
            self.plotsBill[i] = PlotListContainer(str(i+1), self.plotsBill[i].name, self.plotsBill[i].color)

        self.redrawPlotList()

    def minusScaleButtonClicked(self):
        MainWindow.signals.scaleChanged.emit(False)

    def plusScaleButtonClicked(self):
        MainWindow.signals.scaleChanged.emit(True)

class PlotListContainer(QWidget):
    def __init__(self, number, name, color):
        super().__init__()

        self.plotNumber = int(number)
        self.name = name
        self.color = color

        MainWindow.signals.plotColorChangedSignal.connect(self.colorChanged)

        self.numberLabel = QLabel()
        self.numberLabel.setText(number+").")
        self.numberLabel.setFont(TEXT_FONT)
        self.numberLabel.setAlignment(Qt.AlignRight)

        self.plotName = QLabel()
        self.plotName.setFont(QFont("Times New Roman", 16))
        self.plotName.setText(name)

        self.plotName.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.ifVisibleButton = QRadioButton()
        self.ifVisibleButton.setChecked(True)
        self.ifVisibleButton.clicked.connect(self.ifVisibleButtonClicked)
        self.ifVisibleButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.colorButton  = PlotColorChoiceButton(color)
        self.colorButton.clicked.connect(self.colorChoiceButtonClicked)

        self.deletePlotButton = QPushButton()
        self.deletePlotButton.setMinimumSize(22, 22)
        self.deletePlotButton.setMaximumSize(22, 22)
        self.deletePlotButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.deletePlotButton.setIcon(QIcon("cross.png"))
        self.deletePlotButton.clicked.connect(self.deleteButtonClicked)

        self.moreInfoButton = QPushButton()
        self.moreInfoButton.setMinimumSize(22, 22)
        self.moreInfoButton.setMaximumSize(22, 22)
        self.moreInfoButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.moreInfoButton.setIcon(QIcon("plus.png"))
        self.moreInfoButton.clicked.connect(self.moreInfoButtonClicked)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.numberLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.ifVisibleButton, 0, 2, 1, 1)
        self.layout.addWidget(self.plotName, 0, 3, 1, 8)
        self.layout.addWidget(self.colorButton, 0, 11, 1, 1)
        self.layout.addWidget(self.deletePlotButton, 0, 12, 1, 1)
        self.layout.addWidget(self.moreInfoButton, 0, 13, 1, 1)

        self.plotName.setStyleSheet("text-align: left;color: #cccccc; ")
        self.numberLabel.setStyleSheet("text-align: left;color: #cccccc;")
        self.deletePlotButton.setStyleSheet(" border-style: solid; border-width: 1px; border-radius: 11px; background-color: #3c3f41;border-color: #3c3f41")
        self.moreInfoButton.setStyleSheet(" border-style: solid; border-width: 1px; border-radius: 11px; background-color: #3c3f41; border-color: #3c3f41")

    def ifVisibleButtonClicked(self, isChecked):
        MainWindow.signals.plotVisibilityChangedSignal.emit((self.plotNumber, isChecked))

    def colorChanged(self, args):
        self.color = args[1]

    def setButtonColor(self, color):
        self.colorButton.setStyleSheet('''
            background-color: %s;
         ''' % color)

    def colorChoiceButtonClicked(self):
        MainWindow.signals.plotColorChangedSignal.emit((self.plotNumber, self.colorButton.currentColor))

    def deleteButtonClicked(self):
        MainWindow.signals.plotDeletedSignal.emit(self.plotNumber)

    def moreInfoButtonClicked(self):
        pass

class PlotColorChoiceButton(QPushButton):
    def __init__(self, color = '#000000'):
        super().__init__()
        self.setMinimumSize(22, 22)
        self.setMaximumSize(22, 22)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.setButtonColor(color)

        self.currentColor = color

        self.clicked.connect(self.colorChoiceDialog)

    def setButtonColor(self, color):
        self.setStyleSheet('''
            background-color: %s;
            border-radius: 11px;
            border-style: solid;
            border-color: white;
            border-width: 1px;
         ''' %color)

    def colorChoiceDialog(self):
        colorDialog = QColorDialog()
        color = colorDialog.getColor()

        if color.isValid():
            self.currentColor = color.name()
            self.setButtonColor(color.name())

class MenuBar(QMenuBar):
    def __init__(self):
        QMenuBar.__init__(self)

        self.addFileMenu()
        self.addEditMenu()

    def addFileMenu(self):
        fileMenu = self.addMenu('Файл')

        newAction = QAction("&Новый", fileMenu)
        newAction.setShortcut("Ctrl+N")
        # newAction.triggered.connect(qApp.quit)

        openAction = QAction("&Открыть", self)
        openAction.setShortcut("Ctrl+O")

        saveAction = QAction("&Сохранить", self)
        saveAction.setShortcut("Ctrl+S")

        saveAsAction = QAction("&Сохранить как", self)
        saveAsAction.setShortcut("Ctrl+Shift+S")

        printAction = QAction("&Печать", self)
        printAction.setShortcut("Ctrl+P")

        closeAction = QAction("&Выход", self)
        closeAction.setShortcut("Ctrl+Q")

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)

        fileMenu.addSeparator()
        fileMenu.addAction(printAction)

        fileMenu.addSeparator()
        fileMenu.addAction(closeAction)

    def addEditMenu(self):
        editMenu = self.addMenu("Редактирование")

        undoAction = QAction("&Отменить", self)
        undoAction.setShortcut("Ctrl+Z")

        repeatAction = QAction("&Повторить", self)
        repeatAction.setShortcut("Ctrl+Y")

        cutAction = QAction("&Вырезать", self)
        cutAction.setShortcut("Ctrl+X")

        copyAction = QAction("&Копировать", self)
        copyAction.setShortcut("Ctrl+C")

        pasteAction = QAction("&Вставить", self)
        pasteAction.setShortcut("Ctrl+V")

        editMenu.addAction(undoAction)
        editMenu.addAction(repeatAction)

        editMenu.addSeparator()
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)

class PlotCanvas(FigureCanvas):

    def __init__(self, parent):
        self.mainFigure = Figure(dpi=100)

        FigureCanvas.__init__(self, self.mainFigure)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

        self.axes = None

        self.scale = dc.Decimal("50.0")

        self.mainFigure.subplots_adjust(0, 0, 1, 1)

        self.axesPlots = list()

        self.axes = self.mainFigure.add_subplot(111)

        MainWindow.signals.plotVisibilityChangedSignal.connect(self.changePlotsVisibility)
        MainWindow.signals.plotColorChangedSignal.connect(self.changePlorColor)
        MainWindow.signals.plotDeletedSignal.connect(self.deletePlot)
        MainWindow.signals.scaleChanged.connect(self.scaleChanged)

        self.drawAxes()

    def drawAxes(self):
        self.axes.remove()
        self.axes = self.mainFigure.add_subplot(111)

        self.axes.spines["left"].set_position("center")
        self.axes.spines["bottom"].set_position("center")
        self.axes.spines["right"].set_visible("center")
        self.axes.spines["top"].set_visible("center")

        scale = float(self.scale)

        if self.scale >= 1:
            stringScale = str(int(self.scale))

            if self.scale / 10**(len(stringScale)-1) == 1:
                ticksInterval = float(dc.Decimal("10.0")**(len(stringScale)-2))
            else:
                ticksInterval = float(dc.Decimal("10.0")**(len(stringScale)-1))

        else:
            stringScale = str(self.scale)[2:]

            if self.scale * 10 ** len(stringScale) == 1 :
                ticksInterval = float(dc.Decimal("10.0") ** (-len(stringScale) - 1))
            else:
                ticksInterval = float(dc.Decimal("10.0") ** -len(stringScale))

        self.axes.xaxis.set_major_locator(ticker.MultipleLocator(ticksInterval))
        self.axes.xaxis.set_minor_locator(ticker.MultipleLocator(ticksInterval*5))
        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(ticksInterval))
        self.axes.yaxis.set_minor_locator(ticker.MultipleLocator(ticksInterval*5))

        self.axes.minorticks_on()

        self.axes.axis([-scale, scale, -scale, scale])

        interval = 2*scale/400

        xArgs = np.arange(-scale, scale, interval)
        for i in range(len(self.axesPlots)):
            if self.axesPlots[i].isVisible:
                yArgs = [self.axesPlots[i].formula.subs(x, k) for k in xArgs]
                plotColor = self.axesPlots[i].color

                for i in range(len(yArgs)):
                    if yArgs[i] > scale:
                        yArgs[i] = scale+1
                    elif yArgs[i] < -scale:
                        yArgs[i] = -scale-1

                self.axes.plot(xArgs, yArgs, 'k-', color = plotColor)

        self.draw()

    def addPlot(self, text, color):
        text = text.strip()

        textWithoutSpaces = str()
        for i in text:
            if i == ' ':
                continue
            textWithoutSpaces += i
        text = textWithoutSpaces.strip()

        if text == '':
            MainWindow.signals.cleanLineEditSignal.emit()
            return()

        errorMessage = QErrorMessage(self)

        for i in self.axesPlots:
            if text == i.stringFormula:
                errorMessage.setWindowTitle("Ошибка")
                errorMessage.showMessage("Ошибка: Этот график уже существует.\nПовторите попытку.")
                MainWindow.signals.cleanLineEditSignal.emit()
                return()


        ifSymbolError = False
        editedLine = str()
        # ifModuleOpened = False

        for i in range(len(text)):
            if 'x+-*/.()^:12345567890 y=|'.find(text[i]) == -1:
                ifSymbolError = True
            if i > 0 and (text[i - 1] == 'x' or text[i-1] == 'y') and text[i] == '(':
                editedLine += '*' + '('
                continue
            if i > 0 and text[i - 1] == ')' and text[i] == '(':
                editedLine += '*' + '('
                continue
            if i > 0 and '1234567890)'.find(str(text[i - 1])) > 0 and (text[i] == 'x' or text[i] == 'y'):
                editedLine += "*" + "("+text[i]+")"
                continue
            if text[i] == '^':
                editedLine += '**'
                continue
            # if text[i] == '|':
            #     if ifModuleOpened:
            #         editedLine += ')'
            #         ifModuleOpened = False
            #         continue
            #     editedLine+="abs("
            #     ifModuleOpened = True
            #     continue

            if text[i]  == 'x' or text[i] == 'y':
                editedLine += '('+text[i]+')'
                continue
            editedLine += text[i]

        if ifSymbolError:
            errorMessage.setWindowTitle("Ошибка")
            errorMessage.showMessage("Ошибка: введеный текст содержит недопустимые символы.\nПовторите попытку.")
            MainWindow.signals.cleanLineEditSignal.emit()
            return()

        # if ifModuleOpened:
        #     errorMessage.setWindowTitle("Ошибка")
        #     errorMessage.showMessage("Ошибка: обнаружена незакрытый модуль.\nПовторите попытку.")
        #     MainWindow.signals.cleanLineEditSignal.emit()
        #     return ()

        for i in self.axesPlots:
            if i.formula == editedLine:
                errorMessage.setWindowTitle("Ошибка")
                errorMessage.showMessage("Ошибка: Данный график уже существует.")
                MainWindow.signals.cleanLineEditSignal.emit()
                return()

        bracketCounter = 0
        ifBracketError = False

        for i in editedLine:
            if i == '(':
                bracketCounter += 1
            if i == ')':
                bracketCounter -= 1
            if bracketCounter < 0:
                ifBracketError = True
                break

        if bracketCounter != 0 or ifBracketError:
            errorMessage.setWindowTitle("Ошибка")
            errorMessage.showMessage("Ошибка: неправильная расстановка скобок.\nПовторите попытку.")
            MainWindow.signals.cleanLineEditSignal.emit()
            return()

        if len(self.axesPlots) >= MAX_PLOTS:
            errorMessage.setWindowTitle("Ошибка")
            errorMessage.showMessage("Ошибка: Превышено максимальное кол-во графиков.")
            MainWindow.signals.cleanLineEditSignal.emit()
            return()

        axesEquation = AxesEquation(editedLine, text, color)

        MainWindow.signals.plotAddedSignal.emit(axesEquation)

        self.axesPlots.append(axesEquation)

        MainWindow.signals.cleanLineEditSignal.emit()

        self.drawAxes()

    def changePlotsVisibility(self, args):
        self.axesPlots[args[0]-1].isVisible = args[1]
        self.drawAxes()

    def changePlorColor(self, args):
        self.axesPlots[args[0] - 1].changeColor(args[1])
        self.drawAxes()

    def deletePlot(self, index):
        self.axesPlots.pop(index-1)
        print(1)
        self.drawAxes()

    def scaleChanged(self, ifIncrease):
        dc.getcontext().prec = 6
        zoomCoof = dc.Decimal("0.0")

        if self.scale >= 1:
            stringScale = str(int(self.scale))

            if self.scale / 10**(len(stringScale)-1) == 1 and not ifIncrease:
                zoomCoof = dc.Decimal("10.0")**(len(stringScale)-2)
            else:
                zoomCoof = dc.Decimal("10.0")**(len(stringScale)-1)

        else:
            stringScale = str(self.scale)[2:]

            if self.scale * 10 ** len(stringScale) == 1  and not ifIncrease:
                zoomCoof = dc.Decimal("10.0") ** (-len(stringScale) - 1)
            else:
                zoomCoof = dc.Decimal("10.0") ** -len(stringScale)

        if ifIncrease and self.scale < SCALE_MAX:
            self.scale += zoomCoof

        if  not ifIncrease and self.scale > SCALE_MIN:
            self.scale -= zoomCoof

        self.drawAxes()

mainWindow = MainWindow()
startWindow = StartWindow()
aboutProgrammeWindow = AboutProgrammeWindow()

x, y = sp.symbols("x y")

sys.exit(app.exec_())