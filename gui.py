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

        
        self.middleGroupBox = QtWidgets.QGroupBox()
        self.middleLayout = QtWidgets.QGridLayout()
        self.middleLayout.addWidget(self.labelOriginalImage,0,0)
        self.middleLayout.addWidget(self.labelModifiedImage,1,0)
        self.middleGroupBox.setLayout(self.middleLayout)




        self.originalButton = QtWidgets.QPushButton("To Original (Reset Modified)")
        self.originalButton.setDefault(True)
        self.originalButton.clicked.connect(self.toOriginal)

        self.periodicLabel = QtWidgets.QLabel("Periodic Noise Factor:")        
        self.periodicText = QtWidgets.QLineEdit()
        #self.periodicText.setMaximumWidth(100);
        self.periodicText.setText("0.1")
        
        self.periodicButton = QtWidgets.QPushButton("Insert Periodic Noise / Remove using Notch filter")
        self.periodicButton.setDefault(True)
        self.periodicButton.clicked.connect(self.toPeriodic)

        self.periodic2Button = QtWidgets.QPushButton("Insert Periodic Noise / Remove using Mask")
        self.periodic2Button.setDefault(True)
        self.periodic2Button.clicked.connect(self.toPeriodic2)

        #self.labelOriginalImage.setScaledContents(True)

        #This is a sample for converting the original image to a grayscale one
        self.grayButton = QtWidgets.QPushButton("To Gray")
        self.grayButton.setDefault(True)
        self.grayButton.clicked.connect(self.toGray)

        self.histButton = QtWidgets.QPushButton("Histogram (Original Gray)")
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

        self.LoGButton = QtWidgets.QPushButton("Show Laplace of Gaussian (Original)")
        self.LoGButton.setDefault(True)
        self.LoGButton.clicked.connect(self.showLoG)

        self.LaplaceButton = QtWidgets.QPushButton("Show Laplace (Original)")
        self.LaplaceButton.setDefault(True)
        self.LaplaceButton.clicked.connect(self.showLaplace)

        self.sobelEdgeButton = QtWidgets.QPushButton("Show Sobel Edge (Original)")
        self.sobelEdgeButton.setDefault(True)
        self.sobelEdgeButton.clicked.connect(self.showSobelEdge)

        self.sobelAlgorithmButton = QtWidgets.QPushButton("Show Sobel Algorithm (Original)")
        self.sobelAlgorithmButton.setDefault(True)
        self.sobelAlgorithmButton.clicked.connect(self.showSobelAlgorithm)

        self.fourierSpecButton = QtWidgets.QPushButton("Show Fourier")
        self.fourierSpecButton.setDefault(True)
        self.fourierSpecButton.clicked.connect(self.showFourier)


        #self.aboveBottomGroupBox = QtWidgets.QGroupBox()
        self.aboveBottomLayout = QtWidgets.QGridLayout()

        self.aboveBottomLayout.addWidget(self.originalButton,0,0)
        self.aboveBottomLayout.addWidget(self.grayButton,0,1)
        
        self.aboveBottomLayout.addWidget(self.histButton, 0, 2)
        self.aboveBottomLayout.addWidget(self.equalizedHistButton,0,3)
        
        #Periodic noise section
        #self.periodicLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        
        self.aboveBottomLayout.addWidget(self.periodicLabel,1,0)
        self.aboveBottomLayout.addWidget(self.periodicText,1,1)
        self.aboveBottomLayout.addWidget(self.periodicButton,1,2)
        self.aboveBottomLayout.addWidget(self.periodic2Button,1,3)

        #self.aboveBottomLayout.addLayout(self.periodicLayout,1,0,1,4)

        
        self.aboveBottomLayout.addWidget(self.spNoiseButton,2,0)

        self.aboveBottomLayout.addWidget(self.spFixButton,2,1)
        self.aboveBottomLayout.addWidget(self.fourierSpecButton,2,2)
        self.aboveBottomLayout.addWidget(self.LoGButton,2,3)
        self.aboveBottomLayout.addWidget(self.LaplaceButton,3,0)
        self.aboveBottomLayout.addWidget(self.sobelEdgeButton,3,1)
        self.aboveBottomLayout.addWidget(self.sobelAlgorithmButton,3,2)

        #self.aboveBottomGroupBox.setLayout(self.aboveBottomLayout)



        #This is a sample for converting the original image to a grayscale one
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setDefault(True)
        self.saveButton.clicked.connect(self.saveImage)
        
        self.bottomLayout = QtWidgets.QVBoxLayout()
        self.aboveBottomLayout.addWidget(self.saveButton,3,3)

        #Making columns even in width
        self.aboveBottomLayout.setColumnStretch(0,1)
        self.aboveBottomLayout.setColumnStretch(1,1)
        self.aboveBottomLayout.setColumnStretch(2,1)
        self.aboveBottomLayout.setColumnStretch(3,1)


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
        self.originalPlot = self.originalGraphicWidget.addPlot(title='2D spectrum', row=0, col=0)
        self.originalPlotImage = pg.ImageItem()
        self.originalPlot.addItem(self.originalPlotImage)

        self.modifiedGraphicWidget = pg.GraphicsLayoutWidget()
        self.modifiedPlot = self.modifiedGraphicWidget.addPlot(title='2D spectrum', row=0, col=0)
        self.modifiedPlotImage = pg.ImageItem()
        self.modifiedPlot.addItem(self.modifiedPlotImage)

        self.middleLayout.addWidget(self.originalGraphicWidget,0,1)
        self.middleLayout.addWidget(self.modifiedGraphicWidget,1,1)
        self.middleGroupBox.setLayout(self.middleLayout)