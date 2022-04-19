from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import os


class MainUI():
    #Creating, Initializing, and organizing controls of the application
    def setupGUI(self, MainWindow):
        #Setting title and size of spplication window
        MainWindow.setWindowTitle("Image Processing Project - Group 3")
        MainWindow.resize(800, 800)

        #Getting current path and changing icons
        icon = QtGui.QIcon()
        self.curr_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = self.curr_dir + '/icon.png'
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        ##Controls Definition Start
        self.styleTextBoxPath = QtWidgets.QLineEdit()
        self.styleLabelPath = QtWidgets.QLabel("Path:")
        self.browseButton = QtWidgets.QPushButton("Browse")
        self.loadButton = QtWidgets.QPushButton("Load")
        self.topLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.labelOriginalImage = QtWidgets.QLabel()
        self.labelModifiedImage = QtWidgets.QLabel()
        self.middleGroupBox = QtWidgets.QGroupBox()
        self.middleLayout = QtWidgets.QGridLayout()
        self.modifiedRowLabel = QtWidgets.QLabel("Modified Image")
        self.originalButton = QtWidgets.QPushButton("Reset Modified Image")
        self.periodicRowLabel = QtWidgets.QLabel("Periodic Noise")
        self.periodicLabel = QtWidgets.QLabel("Factor:     ")
        self.periodicText = QtWidgets.QLineEdit()
        self.periodicLayout = QtWidgets.QHBoxLayout()
        self.periodicButton = QtWidgets.QPushButton("Add Noise / Remove with Notch filter")
        self.periodic2Button = QtWidgets.QPushButton("Add Noise / Remove with Mask")
        self.histRowLabel = QtWidgets.QLabel("Histograms")
        self.histButton = QtWidgets.QPushButton("Histogram")
        self.equalizedHistButton = QtWidgets.QPushButton("Equalized Histogram")
        self.spRowLabel = QtWidgets.QLabel("Salt and Pepper")
        self.spNoiseButton = QtWidgets.QPushButton("Add Salt and Pepper")
        self.spFixButton = QtWidgets.QPushButton("Fix Salt and Pepper")
        self.LoGOpLabel = QtWidgets.QLabel("Operator Type:")
        self.LoGOpText = QtWidgets.QComboBox()
        self.LoGOpLayout = QtWidgets.QHBoxLayout()
        self.LoGKerLabel = QtWidgets.QLabel("Kernel Size:")
        self.LoGKerText = QtWidgets.QComboBox()
        self.LoGKerLayout = QtWidgets.QHBoxLayout()
        self.LoGausRowLabel = QtWidgets.QLabel("Laplace Of Gaussian")
        self.LoGThreshLabel = QtWidgets.QLabel("Threshold:")
        self.LoGThreshText = QtWidgets.QLineEdit()
        self.LoGThreshLayout = QtWidgets.QHBoxLayout()
        self.LoGButton = QtWidgets.QPushButton("Show Laplace of Gaussian")
        self.LapRowLabel = QtWidgets.QLabel("Laplace")
        self.LapOpLabel = QtWidgets.QLabel("Operator Type:")
        self.LapOpText = QtWidgets.QComboBox()
        self.LapOpLayout = QtWidgets.QHBoxLayout()
        self.LapThreshLabel = QtWidgets.QLabel("Threshold:")
        self.LapThreshText = QtWidgets.QLineEdit()
        self.LapThreshLayout = QtWidgets.QHBoxLayout()
        self.LaplaceButton = QtWidgets.QPushButton("Show Laplace")
        self.sobelRowLabel = QtWidgets.QLabel("Sobel Edge")
        self.sobelLabel = QtWidgets.QLabel("Threshold:")
        self.sobelText = QtWidgets.QLineEdit()
        self.sobelLayout = QtWidgets.QHBoxLayout()
        self.sobelEdgeButton = QtWidgets.QPushButton("Show Sobel Edge")
        self.sobelAlgRowLabel = QtWidgets.QLabel("Sobel Algorithm")
        self.sobelAlgDegreeLabel = QtWidgets.QLabel("Degree:           ")
        self.sobelAlgDegreeText = QtWidgets.QLineEdit()
        self.sobelAlgDegreeLayout = QtWidgets.QHBoxLayout()
        self.sobelAlgThreshLabel = QtWidgets.QLabel("Threshold:")
        self.sobelAlgThreshText = QtWidgets.QLineEdit()
        self.sobelAlgThreshLayout = QtWidgets.QHBoxLayout()
        self.sobelAlgorithmButton = QtWidgets.QPushButton("Show Sobel Algorithm")
        self.saveButton = QtWidgets.QPushButton("Save")
        self.bottomLayout = QtWidgets.QGridLayout()
        self.qPal = QtGui.QPalette()
        self.buFont=QtGui.QFont()
        self.appLayout = QtWidgets.QGridLayout()#Main Layout of the app
        ##Controls Definition End

        
        #Enable Button Controls 
        self.browseButton.setDefault(True)
        self.loadButton.setDefault(True)
        self.originalButton.setDefault(True)
        self.periodicButton.setDefault(True)
        self.periodic2Button.setDefault(True)
        self.histButton.setDefault(True)
        self.equalizedHistButton.setDefault(True)
        self.spNoiseButton.setDefault(True)
        self.spFixButton.setDefault(True)
        self.LoGButton.setDefault(True)
        self.LaplaceButton.setDefault(True)
        self.sobelEdgeButton.setDefault(True)
        self.sobelAlgorithmButton.setDefault(True)
        self.saveButton.setDefault(True)


        #Setting Default values for controls
        self.labelOriginalImage.setPixmap(QtGui.QPixmap())
        self.labelModifiedImage.setPixmap(QtGui.QPixmap())
        self.periodicText.setText("0.1")
        self.LoGOpText.addItems(["eight fields","four fields"])
        self.LoGKerText.addItems(["3","5","7","9","11","13","15","17","19","21","23","25","27","29"])#kernel size
        self.LoGThreshText.setText("10")
        self.LapOpText.addItems(["eight fields","four fields"])
        self.LapThreshText.setText("10")
        self.sobelText.setText("10")
        self.sobelAlgDegreeText.setText("0")
        self.sobelAlgThreshText.setText("10")
        self.qPal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        self.buFont.setBold(True)
        self.buFont.setUnderline(True)


        #Connect Buttons to methods
        self.browseButton.clicked.connect(self.getImagePath)
        self.loadButton.clicked.connect(self.getImageFile)
        self.originalButton.clicked.connect(self.toOriginal)
        self.periodicButton.clicked.connect(self.toPeriodic)
        self.periodic2Button.clicked.connect(self.toPeriodic2)
        self.histButton.clicked.connect(self.getHist)
        self.equalizedHistButton.clicked.connect(self.showEquHistogram)
        self.spNoiseButton.clicked.connect(self.addSaltAndPepper)
        self.spFixButton.clicked.connect(self.fixSaltAndPepper)
        self.LoGButton.clicked.connect(self.showLapOfGaus)
        self.LaplaceButton.clicked.connect(self.showLaplace)
        self.sobelEdgeButton.clicked.connect(self.showSobelEdge)
        self.sobelAlgorithmButton.clicked.connect(self.showSobelAlgorithm)
        self.saveButton.clicked.connect(self.saveImage)


        #Combining Controls in lesser Layout containers (Row Containers)
        self.periodicLayout.addWidget(self.periodicLabel)
        self.periodicLayout.addWidget(self.periodicText)
        self.LoGOpLayout.addWidget(self.LoGOpLabel)
        self.LoGOpLayout.addWidget(self.LoGOpText)
        self.LoGKerLayout.addWidget(self.LoGKerLabel)
        self.LoGKerLayout.addWidget(self.LoGKerText)
        self.LoGThreshLayout.addWidget(self.LoGThreshLabel)
        self.LoGThreshLayout.addWidget(self.LoGThreshText)
        self.LapOpLayout.addWidget(self.LapOpLabel)
        self.LapOpLayout.addWidget(self.LapOpText)
        self.LapThreshLayout.addWidget(self.LapThreshLabel)
        self.LapThreshLayout.addWidget(self.LapThreshText)
        self.sobelLayout.addWidget(self.sobelLabel)
        self.sobelLayout.addWidget(self.sobelText)
        self.sobelAlgDegreeLayout.addWidget(self.sobelAlgDegreeLabel)
        self.sobelAlgDegreeLayout.addWidget(self.sobelAlgDegreeText)
        self.sobelAlgThreshLayout.addWidget(self.sobelAlgThreshLabel)
        self.sobelAlgThreshLayout.addWidget(self.sobelAlgThreshText)

        
        #Adding controls and rows into main containers; top, middle, and bottom
        #Top
        self.topLayout.addWidget(self.styleLabelPath)
        self.topLayout.addWidget(self.styleTextBoxPath)
        self.topLayout.addWidget(self.browseButton)
        self.topLayout.addWidget(self.loadButton)
        #Middle
        self.middleGroupBox.setLayout(self.middleLayout)
        #Bottom
        self.bottomLayout.addWidget(self.histRowLabel,0,0)
        self.bottomLayout.addWidget(self.histButton, 0, 3)
        self.bottomLayout.addWidget(self.equalizedHistButton,0,4)
        self.bottomLayout.addWidget(self.spRowLabel,1,0)
        self.bottomLayout.addWidget(self.spNoiseButton,1,3)
        self.bottomLayout.addWidget(self.spFixButton,1,4)
        self.bottomLayout.addWidget(self.sobelRowLabel,2,0)
        self.bottomLayout.addLayout(self.sobelLayout,2,1)
        self.bottomLayout.addWidget(self.sobelEdgeButton,2,4)
        self.bottomLayout.addWidget(self.sobelAlgRowLabel,3,0)
        self.bottomLayout.addLayout(self.sobelAlgThreshLayout,3,1)
        self.bottomLayout.addLayout(self.sobelAlgDegreeLayout,3,2)
        self.bottomLayout.addWidget(self.sobelAlgorithmButton,3,4)
        self.bottomLayout.addWidget(self.LapRowLabel,4,0)
        self.bottomLayout.addLayout(self.LapThreshLayout,4,1)
        self.bottomLayout.addLayout(self.LapOpLayout,4,2)
        self.bottomLayout.addWidget(self.LaplaceButton,4,4)
        self.bottomLayout.addWidget(self.LoGausRowLabel,5,0)
        self.bottomLayout.addLayout(self.LoGThreshLayout,5,1)
        self.bottomLayout.addLayout(self.LoGOpLayout,5,2)
        self.bottomLayout.addLayout(self.LoGKerLayout,5,3)
        self.bottomLayout.addWidget(self.LoGButton,5,4)
        self.bottomLayout.addWidget(self.periodicRowLabel,6,0)
        self.bottomLayout.addLayout(self.periodicLayout,6,1)
        self.bottomLayout.addWidget(self.periodicButton,6,3)
        self.bottomLayout.addWidget(self.periodic2Button,6,4)
        self.bottomLayout.addWidget(self.modifiedRowLabel,7,0)
        self.bottomLayout.addWidget(self.originalButton,7,3)
        self.bottomLayout.addWidget(self.saveButton,7,4)

        #Setting Row headers
        self.setTitle(self.sobelRowLabel, self.buFont, self.qPal)
        self.setTitle(self.sobelAlgRowLabel, self.buFont, self.qPal)
        self.setTitle(self.LapRowLabel, self.buFont, self.qPal)
        self.setTitle(self.LoGausRowLabel, self.buFont, self.qPal)
        self.setTitle(self.periodicRowLabel, self.buFont, self.qPal)
        self.setTitle(self.spRowLabel, self.buFont, self.qPal)
        self.setTitle(self.modifiedRowLabel, self.buFont, self.qPal)
        self.setTitle(self.histRowLabel, self.buFont, self.qPal)
        
        #Making columns even in width (except for the first/header column)
        self.bottomLayout.setColumnStretch(1,1)
        self.bottomLayout.setColumnStretch(2,1)
        self.bottomLayout.setColumnStretch(3,1)
        self.bottomLayout.setColumnStretch(4,1)

        #Placing main layouts on the app layout
        self.appLayout.addLayout(self.topLayout, 0, 0, 1, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.appLayout.addWidget(self.middleGroupBox, 1, 0, 1, 0)
        self.appLayout.addLayout(self.bottomLayout, 2, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignBottom)

    #Set font and pallette
    def setTitle(self, qLabel, qFont, qPal):
        qLabel.setFont(qFont)
        qLabel.setPalette(qPal)
        
    #Show image and fourrier spectrum on the app screen (Will be run after an image is chosen)
    def activateMiddleParts(self):
        self.originalGraphicWidget = pg.GraphicsLayoutWidget()
        self.originalPlot = self.originalGraphicWidget.addPlot(title='2D Original Spectrum', row=0, col=1)
        self.originalPlotImage = pg.ImageItem()
        self.originalPlot.addItem(self.originalPlotImage)

        self.modifiedGraphicWidget = pg.GraphicsLayoutWidget()
        self.modifiedPlot = self.modifiedGraphicWidget.addPlot(title='2D Modified Spectrum', row=1, col=1)
        self.modifiedPlotImage = pg.ImageItem()
        self.modifiedPlot.addItem(self.modifiedPlotImage)

        #Forcing each item to span over 1 row and 2 columns
        self.middleLayout.addWidget(self.labelOriginalImage,0,0,1,2)
        self.middleLayout.addWidget(self.originalGraphicWidget,0,2,1,2)
        self.middleLayout.addWidget(self.labelModifiedImage,1,0,1,2)
        self.middleLayout.addWidget(self.modifiedGraphicWidget,1,2,1,2)
        self.middleGroupBox.setLayout(self.middleLayout)

    