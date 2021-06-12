import numpy as np
from gui import MainUI
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from vars import Variables
from PIL import Image, ImageQt
import matplotlib.pyplot as plt

#Main Window Class
class ImageProcessingWindow(QDialog, MainUI):
    def __init__(self, parent=None):
        super(ImageProcessingWindow, self).__init__(parent)
        
        #Getting controls for both main window and extra window from the gui.py file
        self.setupGUI(self)
        self.setLayout(self.mainLayout)


    

    

    def loadImages(self):
        #Converting image to qImage and showing it in the image control
        qImage1 = Variables.imageToQImage(Variables.currImage)
        self.labelOriginalImage.setPixmap(QPixmap.fromImage(qImage1).scaled(Variables.image_size, Variables.image_size))
        self.labelOriginalImage.setScaledContents(True)

        qImage2 = Variables.imageToQImage(Variables.modifiedImage)
        self.labelModifiedImage.setPixmap(QPixmap.fromImage(qImage2).scaled(Variables.image_size, Variables.image_size))
        self.labelModifiedImage.setScaledContents(True)

        im_orig = np.mean(np.asarray(Variables.currImage), axis=2) / 255
        im_fft_shift = Variables.get_fft_shift(im_orig)
        self.originalPlotImage.setImage((20*np.log10( 0.1 + im_fft_shift)).astype(int))

        im_modified = np.mean(np.asarray(Variables.modifiedImage), axis=2) / 255
        im_fft_shift_m = Variables.get_fft_shift(im_modified)
        self.modifiedPlotImage.setImage((20*np.log10( 0.1 + im_fft_shift_m)).astype(int))

        

    def getImageFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', QDir.rootPath() , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Open image in the original QPixMap
            self.styleTextBoxPath.setText(fileName)
            
            #Reading into an image object and showing it in the image control
            Variables.currImage = Image.open(fileName)
            self.toOriginal()
            
    def toPeriodic(self):
        im = np.mean(np.asarray(Variables.modifiedImage), axis=2) / 255
        im_noisy = np.copy(im)
        for n in range(im.shape[1]):
            im_noisy[:, n] += np.cos(0.1*np.pi*n)

        Variables.modifiedImage = Image.fromarray(np.uint8(im_noisy)).convert('RGB')

        #set image control to the converted image
        self.loadImages()

    def toOriginal(self):
        Variables.modifiedImage = Variables.currImage.copy()
        self.loadImages()

    


    def toGray(self):
        #call gray transformation method
        Variables.transformToGray(Variables)
        
        #set image control to the converted image
        self.loadImages()

        # self.show_new_window()


    def getHist(self):
        #call gray transformation method
        Variables.transformToGray(Variables)

        grayArray = np.array(Variables.imgToGray(Variables.currImage))
        #Create the histogram from gray image
        plt.hist(grayArray.ravel(), bins=100)
        plt.show()
        #Variables.histImage = Image.fromarray(histNPArray)

    def addSaltAndPepper(self):
        Variables.modifiedImage = Variables.add_sp_noise(Variables.currImage)
        self.loadImages()

    def fixSaltAndPepper(self):
        Variables.modifiedImage = Variables.fix_sp_noise(Variables.currImage)
        self.loadImages()

    def showFourier(self):
        Variables.fourierTransform(Variables.currImage)

    def showEquHistogram(self):
        Variables.equalizedHistogram(Variables.currImage)
    
        

    def saveImage(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', QDir.rootPath() , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Save image
            Variables.modifiedImage.save(fileName)


    def show_new_window(self):
        self.getHist(self)
