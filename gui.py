from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


class MainUI():
    def setupGUI(self, MainWindow):
        #Setting title and size of spplication window
        MainWindow.setWindowTitle("Image Processing Project - Group 3")
        MainWindow.resize(800, 800)

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
        self.loadButton = QtWidgets.QPushButton("Load")
        self.browseButton.setDefault(True)
        self.loadButton.setDefault(True)
        self.browseButton.clicked.connect(self.getImagePath)
        self.loadButton.clicked.connect(self.getImageFile)

        #horizontal layout on top
        self.topLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.topLayout.addWidget(self.styleLabelPath)
        self.topLayout.addWidget(self.styleTextBoxPath)
        self.topLayout.addWidget(self.browseButton)
        self.topLayout.addWidget(self.loadButton)

        #Image Controls
        #self.pixmapImageOriginal = QtGui.QPixmap()
        #self.pixmapImageModified = QtGui.QPixmap()

        #Label container for images
        self.labelOriginalImage = QtWidgets.QLabel()
        self.labelOriginalImage.setPixmap(QtGui.QPixmap())

        self.labelModifiedImage = QtWidgets.QLabel()
        self.labelModifiedImage.setPixmap(QtGui.QPixmap())

        
        self.middleGroupBox = QtWidgets.QGroupBox()
        self.middleLayout = QtWidgets.QGridLayout()
        self.middleGroupBox.setLayout(self.middleLayout)



        self.modifiedRowLabel = QtWidgets.QLabel("Modified Image")
        self.originalButton = QtWidgets.QPushButton("Reset Modified Image")
        self.originalButton.setDefault(True)
        self.originalButton.clicked.connect(self.toOriginal)

        self.periodicRowLabel = QtWidgets.QLabel("Periodic Noise")        
        self.periodicLabel = QtWidgets.QLabel("Factor:     ")        
        self.periodicText = QtWidgets.QLineEdit()
        #self.periodicText.setMaximumWidth(100);
        self.periodicText.setText("0.1")
        self.periodicLayout = QtWidgets.QHBoxLayout()
        self.periodicLayout.addWidget(self.periodicLabel)
        self.periodicLayout.addWidget(self.periodicText)
        
        self.periodicButton = QtWidgets.QPushButton("Add Noise / Remove with Notch filter")
        self.periodicButton.setDefault(True)
        self.periodicButton.clicked.connect(self.toPeriodic)

        self.periodic2Button = QtWidgets.QPushButton("Add Noise / Remove with Mask")
        self.periodic2Button.setDefault(True)
        self.periodic2Button.clicked.connect(self.toPeriodic2)

        #self.labelOriginalImage.setScaledContents(True)

        #This is a sample for converting the original image to a grayscale one
        # self.grayButton = QtWidgets.QPushButton("To Gray")
        # self.grayButton.setDefault(True)
        # self.grayButton.clicked.connect(self.toGray)

        self.histRowLabel = QtWidgets.QLabel("Histograms")
        self.histButton = QtWidgets.QPushButton("Histogram")
        self.histButton.setDefault(True)
        self.histButton.clicked.connect(self.getHist)

        self.equalizedHistButton = QtWidgets.QPushButton("Equalized Histogram")
        self.equalizedHistButton.setDefault(True)
        self.equalizedHistButton.clicked.connect(self.showEquHistogram)


        self.spRowLabel = QtWidgets.QLabel("Salt and Pepper")
        self.spNoiseButton = QtWidgets.QPushButton("Add Salt and Pepper")
        self.spNoiseButton.setDefault(True)
        self.spNoiseButton.clicked.connect(self.addSaltAndPepper)

        self.spFixButton = QtWidgets.QPushButton("Fix Salt and Pepper")
        self.spFixButton.setDefault(True)
        self.spFixButton.clicked.connect(self.fixSaltAndPepper)

        #operator_type="eightfields",kernel_size=3,threshold=-1
        self.LoGOpLabel = QtWidgets.QLabel("Operator Type:")
        self.LoGOpText = QtWidgets.QComboBox()
        self.LoGOpText.addItems(["eight fields","four fields"])
        self.LoGOpLayout = QtWidgets.QHBoxLayout()
        self.LoGOpLayout.addWidget(self.LoGOpLabel)
        self.LoGOpLayout.addWidget(self.LoGOpText)

        self.LoGKerLabel = QtWidgets.QLabel("Kernel Size:")        
        self.LoGKerText = QtWidgets.QComboBox()
        self.LoGKerText.addItems(["1","3","5","7","9","11","13","15","17","19","21"])
        self.LoGKerLayout = QtWidgets.QHBoxLayout()
        self.LoGKerLayout.addWidget(self.LoGKerLabel)
        self.LoGKerLayout.addWidget(self.LoGKerText)

        self.LoGausRowLabel = QtWidgets.QLabel("Laplace Of Gaussian")        
        self.LoGThreshLabel = QtWidgets.QLabel("Threshold:")        
        self.LoGThreshText = QtWidgets.QLineEdit()
        self.LoGThreshText.setText("-1")
        self.LoGThreshLayout = QtWidgets.QHBoxLayout()
        self.LoGThreshLayout.addWidget(self.LoGThreshLabel)
        self.LoGThreshLayout.addWidget(self.LoGThreshText)

        self.LoGButton = QtWidgets.QPushButton("Show Laplace of Gaussian")
        self.LoGButton.setDefault(True)
        self.LoGButton.clicked.connect(self.showLapOfGaus)

        #operator_type="eightfields",threshold=10
        self.LapRowLabel = QtWidgets.QLabel("Laplace")        
        self.LapOpLabel = QtWidgets.QLabel("Operator Type:")
        self.LapOpText = QtWidgets.QComboBox()
        self.LapOpText.addItems(["eight fields","four fields"])
        self.LapOpLayout = QtWidgets.QHBoxLayout()
        self.LapOpLayout.addWidget(self.LapOpLabel)
        self.LapOpLayout.addWidget(self.LapOpText)

        self.LapThreshLabel = QtWidgets.QLabel("Threshold:")
        self.LapThreshText = QtWidgets.QLineEdit()
        self.LapThreshText.setText("10")
        self.LapThreshLayout = QtWidgets.QHBoxLayout()
        self.LapThreshLayout.addWidget(self.LapThreshLabel)
        self.LapThreshLayout.addWidget(self.LapThreshText)

        self.LaplaceButton = QtWidgets.QPushButton("Show Laplace")
        self.LaplaceButton.setDefault(True)
        self.LaplaceButton.clicked.connect(self.showLaplace)


        self.sobelRowLabel = QtWidgets.QLabel("Sobel Edge")
        self.sobelLabel = QtWidgets.QLabel("Threshold:")        
        self.sobelText = QtWidgets.QLineEdit()
        self.sobelText.setText("200")
        self.sobelLayout = QtWidgets.QHBoxLayout()
        self.sobelLayout.addWidget(self.sobelLabel)
        self.sobelLayout.addWidget(self.sobelText)
        
        self.sobelEdgeButton = QtWidgets.QPushButton("Show Sobel Edge")
        self.sobelEdgeButton.setDefault(True)
        self.sobelEdgeButton.clicked.connect(self.showSobelEdge)
        

        self.sobelAlgRowLabel = QtWidgets.QLabel("Sobel Algorithm")
        self.sobelAlgDegreeLabel = QtWidgets.QLabel("Degree:           ")        
        self.sobelAlgDegreeText = QtWidgets.QLineEdit()
        self.sobelAlgDegreeText.setText("0")
        self.sobelAlgDegreeLayout = QtWidgets.QHBoxLayout()
        self.sobelAlgDegreeLayout.addWidget(self.sobelAlgDegreeLabel)
        self.sobelAlgDegreeLayout.addWidget(self.sobelAlgDegreeText)

        self.sobelAlgThreshLabel = QtWidgets.QLabel("Threshold:")
        self.sobelAlgThreshText = QtWidgets.QLineEdit()
        self.sobelAlgThreshText.setText("-1")
        self.sobelAlgThreshLayout = QtWidgets.QHBoxLayout()
        self.sobelAlgThreshLayout.addWidget(self.sobelAlgThreshLabel)
        self.sobelAlgThreshLayout.addWidget(self.sobelAlgThreshText)

        self.sobelAlgorithmButton = QtWidgets.QPushButton("Show Sobel Algorithm")
        self.sobelAlgorithmButton.setDefault(True)
        self.sobelAlgorithmButton.clicked.connect(self.showSobelAlgorithm)

        #self.fourierSpecButton = QtWidgets.QPushButton("Show Fourier")
        #self.fourierSpecButton.setDefault(True)
        #self.fourierSpecButton.clicked.connect(self.showFourier)

        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setDefault(True)
        self.saveButton.clicked.connect(self.saveImage)
        


        #self.aboveBottomGroupBox = QtWidgets.QGroupBox()
        self.aboveBottomLayout = QtWidgets.QGridLayout()

        
        
        
        qPal = QtGui.QPalette()
        qPal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        buFont=QtGui.QFont()
        buFont.setBold(True)
        buFont.setUnderline(True)

        self.sobelRowLabel.setFont(buFont)
        self.sobelRowLabel.setPalette(qPal)
        self.sobelAlgRowLabel.setFont(buFont)
        self.sobelAlgRowLabel.setPalette(qPal)
        self.LapRowLabel.setFont(buFont)
        self.LapRowLabel.setPalette(qPal)
        self.LoGausRowLabel.setFont(buFont)
        self.LoGausRowLabel.setPalette(qPal)
        self.periodicRowLabel.setFont(buFont)
        self.periodicRowLabel.setPalette(qPal)
        self.spRowLabel.setFont(buFont)
        self.spRowLabel.setPalette(qPal)
        self.modifiedRowLabel.setFont(buFont)
        self.modifiedRowLabel.setPalette(qPal)
        self.histRowLabel.setFont(buFont)
        self.histRowLabel.setPalette(qPal)


        self.aboveBottomLayout.addWidget(self.histRowLabel,0,0)
        self.aboveBottomLayout.addWidget(self.histButton, 0, 3)
        self.aboveBottomLayout.addWidget(self.equalizedHistButton,0,4)

        self.aboveBottomLayout.addWidget(self.spRowLabel,1,0)
        self.aboveBottomLayout.addWidget(self.spNoiseButton,1,3)
        self.aboveBottomLayout.addWidget(self.spFixButton,1,4)

        self.aboveBottomLayout.addWidget(self.sobelRowLabel,2,0)
        self.aboveBottomLayout.addLayout(self.sobelLayout,2,1)
        #self.aboveBottomLayout.addWidget(self.sobelText,1,2)
        self.aboveBottomLayout.addWidget(self.sobelEdgeButton,2,4)

        self.aboveBottomLayout.addWidget(self.sobelAlgRowLabel,3,0)
        self.aboveBottomLayout.addLayout(self.sobelAlgThreshLayout,3,1)
        #self.aboveBottomLayout.addWidget(self.sobelAlgThreshText,2,2)
        self.aboveBottomLayout.addLayout(self.sobelAlgDegreeLayout,3,2)
        #self.aboveBottomLayout.addWidget(self.sobelAlgDegreeText,2,4)
        self.aboveBottomLayout.addWidget(self.sobelAlgorithmButton,3,4)
        
        self.aboveBottomLayout.addWidget(self.LapRowLabel,4,0)
        self.aboveBottomLayout.addLayout(self.LapThreshLayout,4,1)
        #self.aboveBottomLayout.addWidget(self.LapThreshText,3,2)
        self.aboveBottomLayout.addLayout(self.LapOpLayout,4,2)
        #self.aboveBottomLayout.addWidget(self.LapOpText,3,4)
        self.aboveBottomLayout.addWidget(self.LaplaceButton,4,4)
        
        self.aboveBottomLayout.addWidget(self.LoGausRowLabel,5,0)
        self.aboveBottomLayout.addLayout(self.LoGThreshLayout,5,1)
        #self.aboveBottomLayout.addWidget(self.LoGThreshText,4,2)
        self.aboveBottomLayout.addLayout(self.LoGOpLayout,5,2)
        #self.aboveBottomLayout.addWidget(self.LoGOpText,4,4)
        self.aboveBottomLayout.addLayout(self.LoGKerLayout,5,3)
        #self.aboveBottomLayout.addWidget(self.LoGKerText,4,6)
        self.aboveBottomLayout.addWidget(self.LoGButton,5,4)
        
        self.aboveBottomLayout.addWidget(self.periodicRowLabel,6,0)
        self.aboveBottomLayout.addLayout(self.periodicLayout,6,1)
        #self.aboveBottomLayout.addWidget(self.periodicText,5,2)
        self.aboveBottomLayout.addWidget(self.periodicButton,6,3)
        self.aboveBottomLayout.addWidget(self.periodic2Button,6,4)

        self.aboveBottomLayout.addWidget(self.modifiedRowLabel,7,0)
        self.aboveBottomLayout.addWidget(self.originalButton,7,3)#,1,2)
        self.aboveBottomLayout.addWidget(self.saveButton,7,4)#,1,2)
        
        #self.aboveBottomLayout.addWidget(self.fourierSpecButton,2,2)
        
        
        
        #self.aboveBottomGroupBox.setLayout(self.aboveBottomLayout)



        
        #self.bottomLayout = QtWidgets.QVBoxLayout()
        #self.aboveBottomLayout.addWidget(self.saveButton,3,3)

        #Making columns even in width
        #self.aboveBottomLayout.setColumnStretch(0,1)
        self.aboveBottomLayout.setColumnStretch(1,1)
        self.aboveBottomLayout.setColumnStretch(2,1)
        self.aboveBottomLayout.setColumnStretch(3,1)
        self.aboveBottomLayout.setColumnStretch(4,1)
        # self.aboveBottomLayout.setColumnStretch(5,1)
        # self.aboveBottomLayout.setColumnStretch(6,1)
        # self.aboveBottomLayout.setColumnStretch(7,1)


        self.mainLayout = QtWidgets.QGridLayout()
        #addLayout(self, QLayout, int, int, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment())
        #addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())
        #addWidget(self, QWidget, int (Row), int (Column), alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment())
        self.mainLayout.addLayout(self.topLayout, 0, 0, 1, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.mainLayout.addWidget(self.middleGroupBox, 1, 0, 1, 0)
        self.mainLayout.addLayout(self.aboveBottomLayout, 2, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignBottom)
        #self.mainLayout.addLayout(self.bottomLayout, 3, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignBottom)

    def showPlot(self):
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