from gui import MainUI
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from vars import Variables
from PIL import Image, ImageCms

#Main Window Class
class ImageProcessingWindow(QDialog, MainUI):
    def __init__(self, parent=None):
        super(ImageProcessingWindow, self).__init__(parent)
        
        #Getting controls from the gui.py file
        self.setupGUI(self)
        self.setLayout(self.mainLayout)


    def imageToQImage(self, pilImage):
        imageBytes = pilImage.convert("RGB").tobytes("raw","RGB")
        qImage = QImage(imageBytes, pilImage.size[0], pilImage.size[1], QtGui.QImage.Format_RGB888)
        return qImage

    

    def loadCurrentImage(self):
        #Converting image to qImage and showing it in the image control
        qImage = self.imageToQImage(Variables.currImage)
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
            Variables.currImage = Image.open(fileName)
            
            self.loadCurrentImage()
            
    
    def toGray(self):
        #Convert current image to grayscale
        Variables.currImage = Variables.currImage.convert('LA')
        
        #set image control to the converted image
        self.loadCurrentImage()
        


    def saveImage(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', QDir.rootPath() , '*.png')

        #If the filename is not empty
        if fileName:
            #Save image
            Variables.currImage.save(fileName)



