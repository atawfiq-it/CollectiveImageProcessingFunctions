from gui import MainUI
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import copy
import threading
import math 

from vars import Variables
from PIL import Image, ImageQt

from scipy import fft

import numpy as np

import matplotlib.pyplot as plt

class LoadImageClass(threading.Thread):
    def __init__(self, uiClass): 
        self.uiClass = uiClass
        threading.Thread.__init__(self) 

    def run(self): 
        self.loadImages()

    def loadImage(self, img, label, plot):
        qImage = ImageQt.ImageQt(img)
        label.setPixmap(QPixmap.fromImage(qImage).scaledToHeight(Variables.image_size))
        
        freq = self.uiClass.get_fft(img)
        plot.setImage((20*np.log10( 0.1 + freq)).astype(int))        

    def loadImages(self):
        self.loadImage(Variables.currImage, self.uiClass.labelOriginalImage, self.uiClass.originalPlotImage)
        self.loadImage(Variables.modifiedImage, self.uiClass.labelModifiedImage, self.uiClass.modifiedPlotImage)

#Main Window Class
class ImageProcessingWindow(QDialog, MainUI):
    def __init__(self, parent=None):
        super(ImageProcessingWindow, self).__init__(parent)
        
        #Getting controls from the gui.py file
        self.setupGUI(self)
        self.setLayout(self.mainLayout)
        
        #fileName = "images/202px-Android_robot.png"
        fileName = "parrot.PNG"
        Variables.currImage = Image.open(fileName).convert('RGB')
        Variables.modifiedImage = Variables.currImage.copy()
        LoadImageClass(self).start()
        
    def getImageFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', QDir.rootPath() , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Open image in the original QPixMap
            self.styleTextBoxPath.setText(fileName)
            
            #Reading into an image object and showing it in the image control
            Variables.currImage = Image.open(fileName).convert('RGB')
            Variables.modifiedImage = Variables.currImage.copy()
            LoadImageClass(self).start()
    
    def get_fft(self, image):
        img_arr = np.array(image)
        if(len(img_arr.shape) == 3): # RGB
            img_gray_scaled = np.mean(img_arr, axis=2) / 255
        else: # Gray
            img_gray_scaled = img_arr / 255

        im_fft = fft.fft2((img_gray_scaled).astype(float))
        return fft.fftshift( im_fft )
    
    def toGray(self):
        Variables.modifiedImage = Variables.currImage.convert('L')
        LoadImageClass(self).start()

    def toPeriodic(self):
        Variables.modifiedImage = Variables.currImage.convert('L')
        im = np.array(Variables.modifiedImage)
        assert(len(im.shape) == 2)

        factor = float(self.periodicText.text())

        im = im.astype(np.float64)
        for n in range(im.shape[0]):
            im[n, :] += np.cos(factor*np.pi*n) * 255

        #im /= (im.max()/255.0)
        
        im = im.astype(np.uint8)
        Variables.modifiedImage = Image.fromarray(np.uint8(im))
        LoadImageClass(self).start()
        
    def removePeriodic(self):
        im = np.array(Variables.modifiedImage)
        assert(len(im.shape) == 2)

        freq = self.get_fft(im)
        freq1 = self.get_fft(np.array(Variables.currImage.convert('L')))
        freq_new = freq - freq1
        
        plt.figure(figsize=(15,10))
        plt.subplot(4,1,1), plt.imshow( (20*np.log10( 0.1 + freq1)).astype(int), cmap=plt.cm.gray)
        plt.subplot(4,1,2), plt.imshow( (20*np.log10( 0.1 + freq)).astype(int), cmap=plt.cm.gray)
        plt.subplot(4,1,3), plt.imshow( (20*np.log10( 0.1 + freq_new)).astype(int), cmap=plt.cm.gray)
        
        limit = 1
        freq2 = freq.copy()
        halfPoint = freq2.shape[0]/2
        halfPointCol = freq2.shape[1]/2
        for i in range(freq2.shape[0]):
            for j in range(freq2.shape[1]):
                if (i > halfPoint-limit and i < halfPoint+limit) or (j > halfPointCol-limit and j < halfPointCol+limit) :
                    freq2[i][j] = 0

        plt.subplot(4,1,4), plt.imshow( (20*np.log10( 0.1 + freq2)).astype(int), cmap=plt.cm.gray)
        plt.show()

        im_restored = np.real(fft.ifft2(fft.ifftshift(freq2)) * 255)
        #im_restored /= (im_restored.max()/255.0)
        im_restored = 255 - im_restored

        Variables.modifiedImage = Image.fromarray(np.uint8(im_restored))
        LoadImageClass(self).start()
        
    def toOriginal(self):
        Variables.modifiedImage = Variables.currImage.copy()
        LoadImageClass(self).start()

    def saveImage(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', QDir.rootPath() , '*.png')

        #If the filename is not empty
        if fileName:
            #Save image
            Variables.modifiedImage.save(fileName)
            