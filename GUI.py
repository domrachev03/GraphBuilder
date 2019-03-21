import sys

import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

app = QApplication(sys.argv)

PROGRAMME_NAME = "Graph builder"
PROGRAMME_ICON = QIcon("ProrgammeLogo.png")
TEXT_FONT = QFont("Times New Roman", 16)
MAX_PLOTS = 10

class Signal(QObject):
    cleanLineEditSignal = pyqtSignal()
    plotAddedSignal = pyqtSignal(tuple)
    plotVisibilityChangedSignal = pyqtSignal(tuple)
    plotColorChangedSignal = pyqtSignal(tuple)
    plotDeletedSignal = pyqtSignal(int)

class MainWindow(QMainWindow):
    signals = Signal()

    def __init__(self):
        super().__init__()

        # self.setGeometry(app.desktop().availableGeometry())
        self.setWindowIcon(PROGRAMME_ICON)
        self.setWindowTitle(PROGRAMME_NAME)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.plotCanvas = PlotCanvas(self)

        self.plotSettings = QWidget()
        self.plotSettingsLayout = QGridLayout()
        self.plotSettings.setLayout(self.plotSettingsLayout)

        self.lineEdit = QLineEdit()
        MainWindow.signals.cleanLineEditSignal.connect(self.clearLineEdit)

        self.yLabel = QLabel("y =")
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

        MainWindow.signals.plotAddedSignal.connect(self.plotAdded)

        MainWindow.signals.plotDeletedSignal.connect(self.plotDeleted)

        self.plotSettingsLayout.addWidget(self.lineEdit, 0, 1, 1, 8)
        self.plotSettingsLayout.addWidget(self.yLabel, 0, 0, 1, 1)
        self.plotSettingsLayout.addWidget(self.plotColorButton, 0, 9, 1, 1)
        self.plotSettingsLayout.addWidget(self.buildButton, 1, 0, 1, 5)
        self.plotSettingsLayout.addWidget(self.discardButton, 1, 5, 1, 5)
        self.plotSettingsLayout.addWidget(self.plotList, 2, 0, 9, 10)

        self.layout = QGridLayout(self.centralWidget)
        self.layout.addWidget(self.plotCanvas, 0, 4, -1, 2)
        self.layout.addWidget(self.plotSettings, 0, 0, -1, 1)
        self.setLayout(self.layout)

        self.menuBar = MenuBar()
        self.setMenuBar(self.menuBar)

        self.show()

    def plotAdded(self, plot):
        newPlot = PlotListContainer(str(len(self.plotsBill)+1), 'y = ' + plot[0], plot[1])

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

        for i in range(len(self.plotsBill), MAX_PLOTS):
            self.plotListLayout.addWidget(QLabel(''), i, 0, 1, 1)

    def buildButtonClicked(self):
        self.plotCanvas.addPlot(self.lineEdit.text(), self.plotColorButton.currentColor)

    def discardButtonClicked(self):
        MainWindow.signals.cleanLineEditSignal.emit()

    def clearLineEdit(self):
        self.lineEdit.clear()

    def plotDeleted(self, index):
        self.plotsBill.pop(index-1)
        for i in range(len(self.plotsBill)):
            self.plotsBill[i] = PlotListContainer(str(i+1), self.plotsBill[i].name, self.plotsBill[i].color)
        self.redrawPlotList()

class PlotListContainer(QWidget):
    def __init__(self, number, name, color):
        super().__init__()

        self.plotNumber = int(number)
        self.name = name
        self.color = color

        self.numberLabel = QLabel()
        self.numberLabel.setText(number+").")
        self.numberLabel.setFont(TEXT_FONT)

        self.plotName = QLabel()
        self.plotName.setFont(TEXT_FONT)
        self.plotName.setText(name)

        self.ifVisibleButton = QRadioButton()
        self.ifVisibleButton.setChecked(True)
        self.ifVisibleButton.clicked.connect(self.ifVisibleButtonClicked)

        self.colorButton  = QPushButton()
        self.setButtonColor(color)
        self.colorButton.clicked.connect(self.colorChoiceDialog)

        self.deletePlotButton = QPushButton()
        self.deletePlotButton.setIcon(QIcon("deleteButton.png"))
        self.deletePlotButton.clicked.connect(self.deleteButtonClicked)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.numberLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.plotName, 0, 2, 1, 6)
        self.layout.addWidget(self.ifVisibleButton, 0, 1, 1, 1)
        self.layout.addWidget(self.colorButton, 0, 8, 1, 1)
        self.layout.addWidget(self.deletePlotButton, 0, 9, 1, 1)

    def ifVisibleButtonClicked(self, isChecked):
        MainWindow.signals.plotVisibilityChangedSignal.emit((self.plotNumber, isChecked))

    def setButtonColor(self, color):
        self.colorButton.setStyleSheet('''
            background-color: %s;
         ''' % color)

    def colorChoiceDialog(self):
        colorDialog = QColorDialog()
        color = colorDialog.getColor()

        if color.isValid():
            self.currentColor = color.name()
            MainWindow.signals.plotColorChangedSignal.emit((self.plotNumber, color.name()))
            self.setButtonColor(color.name())

    def deleteButtonClicked(self):
        MainWindow.signals.plotDeletedSignal.emit(self.plotNumber)

class PlotColorChoiceButton(QPushButton):
    def __init__(self, color = '#000000'):
        super().__init__()

        self.setButtonColor(color)

        self.currentColor = color

        self.clicked.connect(self.colorChoiceDialog)

    def setButtonColor(self, color):
        self.setStyleSheet('''
            background-color: %s;
         ''' %color)

    def colorChoiceDialog(self):
        colorDialog = QColorDialog()
        color = colorDialog.getColor()

        if color.isValid():
            self.currentColor = color.name()
            self.setButtonColor(color.name())

class MenuBar(QMenuBar, MainWindow):
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

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.axes = None

        self.mainFigure.subplots_adjust(0, 0, 1, 1)

        self.axesPlots = list()

        self.axes = self.mainFigure.add_subplot(111)

        MainWindow.signals.plotVisibilityChangedSignal.connect(self.changePlotsVisibility)
        MainWindow.signals.plotColorChangedSignal.connect(self.changePlorColor)
        MainWindow.signals.plotDeletedSignal.connect(self.deletePlot)

        self.drawAxes()

    def drawAxes(self):
        self.axes.remove()
        self.axes = self.mainFigure.add_subplot(111)

        self.axes.spines["left"].set_position("center")
        self.axes.spines["bottom"].set_position("center")
        self.axes.spines["right"].set_visible("center")
        self.axes.spines["top"].set_visible("center")

        plt.xticks(np.arange(-90, 90, 1))
        plt.yticks(np.arange(-90, 90, 1))

        self.axes.axis([-100, 100, -100, 100])

        for i in range(len(self.axesPlots)):
            if self.axesPlots[i][2]:
                xArgs = np.arange(-120., 120., 0.2)
                yArgs = [(eval(self.axesPlots[i][0].replace('x', str(k)))) for k in xArgs]

                plotColor = self.axesPlots[i][1]

                self.axes.plot(xArgs, yArgs, 'k-', color = plotColor)
        self.draw()

    def addPlot(self, text, color):
        text = text.strip()

        textWithoutSpaces = str()
        for i in text:
            if i == ' ':
                continue
            textWithoutSpaces += i
        text = textWithoutSpaces

        if text.strip() == '':
            MainWindow.signals.cleanLineEditSignal.emit()
            return()

        errorMessage = QErrorMessage(self)

        ifSymbolError = False
        editedLine = str()
        for i in range(len(text)):
            if 'x+-*/.,()^:12345567890 '.find(text[i]) == -1:
                ifSymbolError = True
            if i > 0 and text[i - 1] == 'x' and text[i] == '(':
                editedLine += '*' + '('
                continue
            if i > 0 and text[i - 1] == ')' and text[i] == '(':
                editedLine += '*' + '('
                continue
            if i > 0 and '1234567890)'.find(str(text[i - 1])) > 0 and text[i] == 'x':
                editedLine += "*" + "(x)"
                continue
            if text[i] == '^':
                editedLine += '**'
                continue
            if text[i] == 'x':
                editedLine += '(x)'
                continue
            editedLine += text[i]

        if ifSymbolError:
            errorMessage.setWindowTitle("Ошибка")
            errorMessage.showMessage("Ошибка: введеный текст содержит недопустимые символы.\nПовторите попытку.")
            MainWindow.signals.cleanLineEditSignal.emit()
            return()

        for i in self.axesPlots:
            if i[0] == editedLine:
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

        if len(self.axesPlots) > MAX_PLOTS:
            errorMessage.setWindowTitle("Ошибка")
            errorMessage.showMessage("Ошибка: Превышено максимальное кол-во графиков.")
            MainWindow.signals.cleanLineEditSignal.emit()
            return()

        MainWindow.signals.plotAddedSignal.emit((text, color, True))

        self.axesPlots.append([editedLine, color, True])

        MainWindow.signals.cleanLineEditSignal.emit()

        self.drawAxes()

    def changePlotsVisibility(self, args):
        self.axesPlots[args[0]-1][2] = args[1]
        self.drawAxes()

    def changePlorColor(self, args):
        self.axesPlots[args[0] - 1][1] = args[1]
        self.drawAxes()

    def deletePlot(self, index):
        self.axesPlots.pop(index-1)
        self.drawAxes()

mainWindow = MainWindow()
sys.exit(app.exec_())