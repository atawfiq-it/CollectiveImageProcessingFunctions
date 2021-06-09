from gui import MainUI
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from vars import Variables
from PIL import Image, ImageQt

from scipy import fft

import numpy as np

#Main Window Class
class ImageProcessingWindow(QDialog, MainUI):
    def __init__(self, parent=None):
        super(ImageProcessingWindow, self).__init__(parent)
        
        #Getting controls from the gui.py file
        self.setupGUI(self)
        self.setLayout(self.mainLayout)

    def imageToQImage(self, pilImage):
        qImage = ImageQt.ImageQt(pilImage)
        #qImage = QtGui.QPixmap.fromImage(qim)

        #imageBytes = pilImage.convert("RGB").tobytes("raw","RGB")
        #qImage = QImage(imageBytes, pilImage.size[0], pilImage.size[1], QtGui.QImage.Format_RGB888)
        return qImage

    def get_fft_shift(self, im):
        im_fft = fft.fft2((im).astype(float))
        return fft.fftshift( im_fft )

    def loadImages(self):
        #Converting image to qImage and showing it in the image control
        qImage = self.imageToQImage(Variables.currImage)
        self.labelOriginalImage.setPixmap(QPixmap.fromImage(qImage).scaled(Variables.image_size, Variables.image_size))
        self.labelOriginalImage.setScaledContents(True)
        
        qImage = self.imageToQImage(Variables.modifiedImage)
        self.labelModifiedImage.setPixmap(QPixmap.fromImage(qImage).scaled(Variables.image_size, Variables.image_size))
        self.labelModifiedImage.setScaledContents(True)        
        
        im = np.mean(np.asarray(Variables.currImage), axis=2) / 255
        im_fft_shift = self.get_fft_shift(im)
        self.originalPlotImage.setImage((20*np.log10( 0.1 + im_fft_shift)).astype(int))

        im_m = np.mean(np.asarray(Variables.modifiedImage), axis=2) / 255
        im_fft_shift_m = self.get_fft_shift(im_m)
        self.modifiedPlotImage.setImage((20*np.log10( 0.1 + im_fft_shift_m)).astype(int))

    def getImageFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', QDir.rootPath() , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Open image in the original QPixMap
            self.styleTextBoxPath.setText(fileName)
            
            #Reading into an image object and showing it in the image control
            Variables.currImage = Image.open(fileName)
            Variables.modifiedImage = Image.open(fileName)

            self.loadImages()
            
    
    def toGray(self):
        #Convert current image to grayscale
        Variables.modifiedImage = Variables.modifiedImage.convert('L')
        
        #set image control to the converted image
        self.loadImages()

    def toPeriodic(self):
        im = np.mean(np.asarray(Variables.modifiedImage), axis=2) / 255
        im_noisy = np.copy(im)
        for n in range(im.shape[1]):
            im_noisy[:, n] += np.cos(0.1*np.pi*n)

        Variables.modifiedImage = Image.fromarray(np.uint8(im_noisy)).convert('RGB')
        
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
            