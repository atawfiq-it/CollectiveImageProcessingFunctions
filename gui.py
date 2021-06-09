from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

import numpy as np

class MainUI():
    
    def setupGUI(self, MainWindow):
        #Setting title and size of spplication window
        MainWindow.setWindowTitle("Image Processing Project - Group 3")
        MainWindow.resize(800, 800)

        icon = QtGui.QIcon()
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

        #Label container for images
        self.labelOriginalImage = QtWidgets.QLabel()
        self.labelOriginalImage.setPixmap(QtGui.QPixmap())

        self.labelModifiedImage = QtWidgets.QLabel()
        self.labelModifiedImage.setPixmap(QtGui.QPixmap())
        
        originalGraphicWidget = pg.GraphicsLayoutWidget()
        originalPlot = originalGraphicWidget.addPlot(title='2D spectrum', row=0, col=0)
        self.originalPlotImage = pg.ImageItem()
        originalPlot.addItem(self.originalPlotImage)
        
        modifiedGraphicWidget = pg.GraphicsLayoutWidget()
        modifiedPlot = modifiedGraphicWidget.addPlot(title='2D spectrum', row=0, col=0)
        self.modifiedPlotImage = pg.ImageItem()
        modifiedPlot.addItem(self.modifiedPlotImage)


        #This is a sample for converting the original image to a grayscale one
        self.originalButton = QtWidgets.QPushButton("To Original")
        self.originalButton.setDefault(True)
        self.originalButton.clicked.connect(self.toOriginal)

        self.grayButton = QtWidgets.QPushButton("To Gray")
        self.grayButton.setDefault(True)
        self.grayButton.clicked.connect(self.toGray)

        self.periodicButton = QtWidgets.QPushButton("Periodic Noise")
        self.periodicButton.setDefault(True)
        self.periodicButton.clicked.connect(self.toPeriodic)

        #This is a sample for converting the original image to a grayscale one
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setDefault(True)
        self.saveButton.clicked.connect(self.saveImage)
                
        self.bottomLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.bottomLayout.addWidget(self.originalButton)
        self.bottomLayout.addWidget(self.grayButton)
        self.bottomLayout.addWidget(self.periodicButton)
        self.bottomLayout.addWidget(self.saveButton)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.mainLayout.addWidget(self.labelOriginalImage,1,0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(originalGraphicWidget,1,1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelModifiedImage,2,0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(modifiedGraphicWidget,2,1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addLayout(self.bottomLayout,3,0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)

        