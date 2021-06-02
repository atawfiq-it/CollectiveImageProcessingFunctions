from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.browseButton.setDefault(True)
        self.browseButton.clicked.connect(self.getImageFile)

        #horizontal layout on top
        self.topLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.topLayout.addWidget(self.styleLabelPath)
        self.topLayout.addWidget(self.styleTextBoxPath)
        self.topLayout.addWidget(self.browseButton)

        #Image Control
        self.pixmapImageOriginal = QtGui.QPixmap()

        #Label container for images
        self.labelImageResult = QtWidgets.QLabel()
        #width = 300
        #height = 300
        #self.labelImageResult.setFixedSize(width,height)
        #self.labelImageResult.setFixedHeight(height)
        
        self.labelImageResult.setPixmap(self.pixmapImageOriginal)
        #self.labelImageResult.setScaledContents(True)

        #This is a sample for converting the original image to a grayscale one
        self.grayButton = QtWidgets.QPushButton("To Gray")
        self.grayButton.setDefault(True)
        self.grayButton.clicked.connect(self.toGray)

        #This is a sample for converting the original image to a grayscale one
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setDefault(True)
        self.saveButton.clicked.connect(self.saveImage)
        
        self.bottomLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.bottomLayout.addWidget(self.grayButton)
        self.bottomLayout.addWidget(self.saveButton)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.mainLayout.addWidget(self.labelImageResult,1,0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addLayout(self.bottomLayout,2,0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)

        