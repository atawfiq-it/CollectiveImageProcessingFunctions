from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image, ImageCms

#Main Window Class
class ImageProcessingWindow(QDialog):
    def __init__(self, parent=None):
        super(ImageProcessingWindow, self).__init__(parent)

        self.resize(800, 800)
        icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("path"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        mode = 'RGB'
        size = (1, 1)
        color = (0, 0, 0)
        self.currImage = Image.new(mode, size, color)

        #Textbox containing the path
        self.styleTextBoxPath = QLineEdit()

        self.styleLabelPath = QLabel("&Path:")
        
        #press Alt+P to activate the browse textbox
        self.styleLabelPath.setBuddy(self.styleTextBoxPath)

        #Browse button and action referencing the getImageFile function
        self.browseButton = QPushButton("Browse")
        self.browseButton.setDefault(True)
        self.browseButton.clicked.connect(self.getImageFile)

        #horizontal layout on top
        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.styleLabelPath)
        self.topLayout.addWidget(self.styleTextBoxPath)
        self.topLayout.addWidget(self.browseButton)
        #topLayout.addStretch(1)

        #Image Control
        self.pixmapImageOriginal = QtGui.QPixmap()
        
        
        #Label container for images
        self.labelImageResult = QLabel()
        #width = 300
        #height = 300
        #self.labelImageResult.setFixedSize(width,height)
        #self.labelImageResult.setFixedHeight(height)

        self.labelImageResult.setPixmap(self.pixmapImageOriginal)
        #self.labelImageResult.setScaledContents(True)

        
        #This is a sample for converting the original image to a grayscale one
        self.grayButton = QPushButton("To Gray")
        self.grayButton.setDefault(True)
        self.grayButton.clicked.connect(self.toGray)
        
        #This is a sample for converting the original image to a grayscale one
        self.saveButton = QPushButton("Save")
        self.saveButton.setDefault(True)
        self.saveButton.clicked.connect(self.saveImage)
        
        self.bottomLayout = QVBoxLayout()
        self.bottomLayout.addWidget(self.grayButton)
        self.bottomLayout.addWidget(self.saveButton)
        
        #addLayout/addWidget
        #(QLayout *layout, int row, int column, Qt::Alignment alignment = Qt::Alignment())
        #(QLayout *layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())
        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0, 1, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mainLayout.addWidget(self.labelImageResult,1,0,Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addLayout(self.bottomLayout,2,0, 1, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Image Processing Project - Group 3")


    def imageToQImage(self, pilImage):
        imageBytes = pilImage.convert("RGB").tobytes("raw","RGB")
        qImage = QImage(imageBytes, pilImage.size[0], pilImage.size[1], QtGui.QImage.Format_RGB888)
        return qImage

    

    def loadCurrentImage(self):
        #Converting image to qImage and showing it in the image control
        qImage = self.imageToQImage(self.currImage)
        self.pixmapImageOriginal = QPixmap.fromImage(qImage)
        self.labelImageResult.setPixmap(self.pixmapImageOriginal)
        self.labelImageResult.setScaledContents(True)

        

    def getImageFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', QDir.rootPath() , '*.png')

        #If the filename is not empty
        if fileName:
            #Open image in the original QPixMap
            self.styleTextBoxPath.setText(fileName)
            
            #Reading into an image object and showing it in the image control
            self.currImage = Image.open(fileName)
            
            self.loadCurrentImage()
            
    
    def toGray(self):
        #Convert current image to grayscale
        self.currImage = self.currImage.convert('LA')
        
        #set image control to the converted image
        self.loadCurrentImage()
        


    def saveImage(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', QDir.rootPath() , '*.png')

        #If the filename is not empty
        if fileName:
            #Save image
            self.currImage.save(fileName)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    ip_windows = ImageProcessingWindow()
    ip_windows.show()
    sys.exit(app.exec_()) 
