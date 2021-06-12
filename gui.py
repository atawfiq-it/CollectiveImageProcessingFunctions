from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


class MainUI():
    def setupGUI(self, MainWindow):
        #Setting title and size of spplication window
        MainWindow.setWindowTitle("Image Processing Project - Group 3")
        MainWindow.resize(1000, 1000)

        icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("path"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        #Textbox containing the path
        self.styleTextBoxPath = QtWidgets.QLineEdit()
        self.styleLabelPath = QtWidgets.QLabel("&Path:")

        #press Alt+P to activate the browse textbox
        self.styleLabelPath.setBuddy(self.styleTextBoxPath)

        #Browse button and action referencing the getImageFile function
        self.browseButton = QtWidgets.QPushButton("Browse")
        self.browseButton.setDefault(True)
        self.browseButton.clicked.connect(self.getImageFile)

        #horizontal layout on top
        self.topLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.topLayout.addWidget(self.styleLabelPath)
        self.topLayout.addWidget(self.styleTextBoxPath)
        self.topLayout.addWidget(self.browseButton)

        #Image Controls
        #self.pixmapImageOriginal = QtGui.QPixmap()
        #self.pixmapImageModified = QtGui.QPixmap()

        #Label container for images
        self.labelOriginalImage = QtWidgets.QLabel()
        self.labelOriginalImage.setPixmap(QtGui.QPixmap())

        self.labelModifiedImage = QtWidgets.QLabel()
        self.labelModifiedImage.setPixmap(QtGui.QPixmap())

        self.originalGraphicWidget = pg.GraphicsLayoutWidget()
        self.originalPlot = self.originalGraphicWidget.addPlot(title='2D spectrum', row=0, col=0)
        self.originalPlotImage = pg.ImageItem()
        self.originalPlot.addItem(self.originalPlotImage)

        self.modifiedGraphicWidget = pg.GraphicsLayoutWidget()
        self.modifiedPlot = self.modifiedGraphicWidget.addPlot(title='2D spectrum', row=0, col=0)
        self.modifiedPlotImage = pg.ImageItem()
        self.modifiedPlot.addItem(self.modifiedPlotImage)

        self.originalButton = QtWidgets.QPushButton("To Original")
        self.originalButton.setDefault(True)
        self.originalButton.clicked.connect(self.toOriginal)

        self.periodicButton = QtWidgets.QPushButton("Periodic Noise")
        self.periodicButton.setDefault(True)
        self.periodicButton.clicked.connect(self.toPeriodic)

        #self.labelOriginalImage.setScaledContents(True)

        #This is a sample for converting the original image to a grayscale one
        self.grayButton = QtWidgets.QPushButton("To Gray")
        self.grayButton.setDefault(True)
        self.grayButton.clicked.connect(self.toGray)

        self.histButton = QtWidgets.QPushButton("Histogram")
        self.histButton.setDefault(True)
        self.histButton.clicked.connect(self.getHist)

        self.equalizedHistButton = QtWidgets.QPushButton("Equalized Histogram")
        self.equalizedHistButton.setDefault(True)
        self.equalizedHistButton.clicked.connect(self.showEquHistogram)

        self.spNoiseButton = QtWidgets.QPushButton("Add Salt & Pepper")
        self.spNoiseButton.setDefault(True)
        self.spNoiseButton.clicked.connect(self.addSaltAndPepper)

        self.spFixButton = QtWidgets.QPushButton("Fix Salt & Pepper")
        self.spFixButton.setDefault(True)
        self.spFixButton.clicked.connect(self.fixSaltAndPepper)

        self.fourierSpecButton = QtWidgets.QPushButton("Show Fourier")
        self.fourierSpecButton.setDefault(True)
        self.fourierSpecButton.clicked.connect(self.showFourier)

        #This is a sample for converting the original image to a grayscale one
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setDefault(True)
        self.saveButton.clicked.connect(self.saveImage)
        
        self.bottomLayout = QtWidgets.QVBoxLayout()
        self.bottomLayout.addWidget(self.originalButton)
        self.bottomLayout.addWidget(self.grayButton)
        self.bottomLayout.addWidget(self.periodicButton)
        self.bottomLayout.addWidget(self.histButton)
        self.bottomLayout.addWidget(self.equalizedHistButton)
        self.bottomLayout.addWidget(self.spNoiseButton)
        self.bottomLayout.addWidget(self.spFixButton)
        self.bottomLayout.addWidget(self.fourierSpecButton)
        self.bottomLayout.addWidget(self.saveButton)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.mainLayout.addWidget(self.labelOriginalImage,1,0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.originalGraphicWidget,1,1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelModifiedImage,2,0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.modifiedGraphicWidget,2,1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addLayout(self.bottomLayout,3,0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        