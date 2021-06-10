from gui import MainUI
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from vars import Variables
from PIL import Image, ImageQt

from scipy import fft

import numpy as np

import matplotlib.pyplot as plt

#Main Window Class
class ImageProcessingWindow(QDialog, MainUI):
    def __init__(self, parent=None):
        super(ImageProcessingWindow, self).__init__(parent)
        
        #Getting controls from the gui.py file
        self.setupGUI(self)
        self.setLayout(self.mainLayout)
        
        fileName = "images/403px-Android_robot.png"
        Variables.currImage = Image.open(fileName).convert('RGB')
        Variables.modifiedImage = Image.open(fileName).convert('RGB')
        self.loadImages()

    def imageToQImage(self, pilImage):
        qImage = ImageQt.ImageQt(pilImage)
        return qImage

    def get_fft(self, image_to_process):
        array = np.array(image_to_process)
        if(len(array.shape) == 3): # RGB
            im = np.mean(array, axis=2) / 255
        else: # Gray
            im = array

        im_fft = fft.fft2((im).astype(float))
        return fft.fftshift( im_fft )

    def loadImages(self):
        #Converting image to qImage and showing it in the image control
        qImage = self.imageToQImage(Variables.currImage)
        self.labelOriginalImage.setPixmap(QPixmap.fromImage(qImage).scaledToHeight(Variables.image_size))
        self.labelOriginalImage.setScaledContents(True)
        
        qImage = self.imageToQImage(Variables.modifiedImage)
        self.labelModifiedImage.setPixmap(QPixmap.fromImage(qImage).scaledToHeight(Variables.image_size))
        self.labelModifiedImage.setScaledContents(True)        
        
        self.originalPlotImage.setImage(self.get_fft(Variables.currImage))
        self.modifiedPlotImage.setImage(self.get_fft(Variables.modifiedImage))


    def getImageFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', QDir.rootPath() , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Open image in the original QPixMap
            self.styleTextBoxPath.setText(fileName)
            
            #Reading into an image object and showing it in the image control
            Variables.currImage = Image.open(fileName).convert('RGB')
            Variables.modifiedImage = Image.open(fileName).convert('RGB')

            self.loadImages()
            
    
    def toGray(self):
        Variables.modifiedImage = Variables.modifiedImage.convert('L')
        self.loadImages()

    def toPeriodic(self):
        self.toGray()
        array = np.array(Variables.modifiedImage)
        assert(len(array.shape) == 2)
        im = array

        im_noisy = np.copy(im)
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                im_noisy[i, j] += np.cos(0.1*np.pi*j)

        Variables.modifiedImage = Image.fromarray(np.uint8(im_noisy))
        
        #Variables.modifiedImage = Variables.modifiedImage.convert('RGB')

        aaaa = Variables.currImage
        bbbb = Variables.modifiedImage
        
        #set image control to the converted image
        self.loadImages()
        
    def toOriginal(self):
        Variables.modifiedImage = Variables.currImage
        self.loadImages()

    def saveImage(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', QDir.rootPath() , '*.png')

        #If the filename is not empty
        if fileName:
            #Save image
            Variables.modifiedImage.save(fileName)
            