from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

import numpy as np

class MainUI():
    
    def createButton(self, text, cb):
        button = QtWidgets.QPushButton(text)
        button.setDefault(True)
        button.clicked.connect(cb)
        return button
    
    def createPlot(self):
        label = QtWidgets.QLabel()
        label.setPixmap(QtGui.QPixmap())
        widget = pg.GraphicsLayoutWidget()
        plot = widget.addPlot(title='2D spectrum', row=0, col=0)
        plotImage = pg.ImageItem(border='w')
        plot.addItem(plotImage)
        return (widget, label, plotImage)
    
    def createBrowseLayer(self):
        self.styleLabelPath = QtWidgets.QLabel("&Path:")
        self.styleTextBoxPath = QtWidgets.QLineEdit()

        #press Alt+P to activate the browse textbox
        self.styleLabelPath.setBuddy(self.styleTextBoxPath)

        self.browseButton = self.createButton("Browse", self.getImageFile)

        layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        layout.addWidget(self.styleLabelPath)
        layout.addWidget(self.styleTextBoxPath)
        layout.addWidget(self.browseButton)
        return layout
    
    def createPeriodicLayer(self):
        self.periodicLabel = QtWidgets.QLabel("&Periodic Noise Factor(<1):")        
        self.periodicText = QtWidgets.QLineEdit()
        self.periodicText.setText("0.1")
        
        self.periodicButton = self.createButton("Periodic Noise", self.toPeriodic)
        self.removePeriodicButton = self.createButton("Remove Noise", self.removePeriodic)
        
        layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        layout.addWidget(self.periodicLabel)
        layout.addWidget(self.periodicText)
        layout.addWidget(self.periodicButton)
        layout.addWidget(self.removePeriodicButton)
        return layout

    def createMainButtonLayer(self):
        self.originalButton = self.createButton("To Original", self.toOriginal)
        self.grayButton = self.createButton("To Gray", self.toGray)
        self.saveButton = self.createButton("Save", self.saveImage)
         
        layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        layout.addWidget(self.originalButton)
        layout.addWidget(self.grayButton)
        layout.addWidget(self.saveButton)
        return layout
    
    def setupGUI(self, MainWindow):
        MainWindow.setWindowTitle("Image Processing Project - Group 3")
        MainWindow.resize(800, 800)

        icon = QtGui.QIcon()
        self.setWindowIcon(icon)

        topLayout = self.createBrowseLayer()
        
        (originalGraphicWidget, self.labelOriginalImage, self.originalPlotImage) = self.createPlot()
        (modifiedGraphicWidget, self.labelModifiedImage, self.modifiedPlotImage) = self.createPlot()
        
        mainByuttonLayer = self.createMainButtonLayer()
        periodicLayout = self.createPeriodicLayer()
        
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(topLayout, 0, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.mainLayout.addWidget(self.labelOriginalImage,1,0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(originalGraphicWidget,1,1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelModifiedImage,2,0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(modifiedGraphicWidget,2,1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addLayout(mainByuttonLayer, 3, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.mainLayout.addLayout(periodicLayout, 4,0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        