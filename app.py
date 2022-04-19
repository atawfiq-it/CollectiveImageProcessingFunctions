import os
import PIL
from PyQt5 import QtCore
import numpy as np
from gui import MainUI
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from backend import Backend
from PIL import Image
import matplotlib.pyplot as plt

#Main Window Class
class ImageProcessingWindow(QDialog, MainUI):
    def __init__(self, parent=None):
        super(ImageProcessingWindow, self).__init__(parent)
        
        #Getting controls for both main window and extra window from the gui.py file
        self.setupGUI(self)
        self.setLayout(self.appLayout)
        #Disable question mark on top, enable minimize, maximize, and close buttons
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | 
        QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint| QtCore.Qt.WindowMinimizeButtonHint)

    #Load images into image controls
    def loadImages(self):
        #Converting image to qImage and showing it in the image control
        qImage1 = Backend.imageToQImage(Backend.currImage)
        self.labelOriginalImage.setPixmap(QPixmap.fromImage(qImage1).scaled(Backend.image_size, Backend.image_size))
        self.labelOriginalImage.setScaledContents(True)

        qImage2 = Backend.imageToQImage(Backend.modifiedImage)
        self.labelModifiedImage.setPixmap(QPixmap.fromImage(qImage2).scaled(Backend.image_size, Backend.image_size))
        self.labelModifiedImage.setScaledContents(True)

        #Show plot images after an image is loaded
        self.activateMiddleParts()
        im_ori_arr = np.asarray(Backend.currImage.getdata()).reshape(Backend.currImage.size[1], Backend.currImage.size[0], -1)
        im_orig = np.mean(im_ori_arr, axis=2) / 255
        im_fft_shift = Backend.get_fft_shift(im_orig)
        self.originalPlotImage.setImage((20*np.log10( 0.1 + im_fft_shift)).astype(int))

        im_mod_arr = np.asarray(Backend.modifiedImage.getdata()).reshape(Backend.modifiedImage.size[1], Backend.modifiedImage.size[0], -1)
        im_modified = np.mean(im_mod_arr, axis=2) / 255
        im_fft_shift_m = Backend.get_fft_shift(im_modified)
        self.modifiedPlotImage.setImage((20*np.log10( 0.1 + im_fft_shift_m)).astype(int))

        #An image has been loaded successfully
        Backend.default_image = False

    #Read and place image path in the textbox (also loads the images)
    def getImagePath(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', os.path.dirname(os.path.realpath(__file__)) , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Open image in the original QPixMap
            self.styleTextBoxPath.setText(fileName)
            #Open image if selected through browse directly
            self.getImageFile()
            

    def getImageFile(self):
        imgPath = self.styleTextBoxPath.text().upper()
        if len(imgPath) == 0:
            Backend.showMessage("Empty Path","Kindly fill in the file path or use the Browse button to select a file.")
            return
        elif not imgPath.endswith(".PNG") and not imgPath.endswith(".JPG") and not imgPath.endswith(".JPEG"):
            Backend.showMessage("Incorrect Type","The provided path must be to a PNG/JPG/JPEG image file. Please provide a valid path to an image file.")
            return

        #Reading into an image object and showing it in the image control
        try:
            Backend.currImage = Image.open(self.styleTextBoxPath.text()).convert("L")
            #Copy original image to the modified
            self.toOriginal(True)#Skip Check of existing image
        except FileNotFoundError:
            Backend.showMessage("Incorrect Path","The provided file path is not correct. Please provide a valid file path.")
            return
        except PIL.UnidentifiedImageError:
            Backend.showMessage("Incorrect Type","The provided file can not be interpreted as a valid image. Please provide a valid path to an image file.")
            return
            

    #Call functions from backend (Start)
    def toPeriodic(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        Backend.periodic_noise(self, Backend.currImage)


    def toPeriodic2(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        Backend.periodic2_noise(self, Backend.currImage)

        #set image control to the converted image
        self.loadImages()

    def toOriginal(self, skip=False):
        #Check if an image has been loaded
        if Backend.default_image == True and skip == False:
            Backend.noImageSelected()
            return
        #Copy image from original to modified
        Backend.modifiedImage = Backend.currImage.copy()
        #Reload image
        self.loadImages()

    def toGray(self):
        #call gray transformation method
        Backend.transformToGray(Backend)
        
        #set image control to the converted image
        self.loadImages()
        

    def getHist(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return

        #call gray transformation method
        Backend.transformToGray(Backend)

        grayArray = np.array(Backend.currImage)
        
        plt.close("all")#Close existing plots before creating a new one
        #Create the histogram from gray image
        plt.hist(grayArray.ravel(), bins=100)
        plt.show()
        #Backend.histImage = Image.fromarray(histNPArray)

    def addSaltAndPepper(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        Backend.modifiedImage = Backend.add_sp_noise(Backend.modifiedImage)
        self.loadImages()

    def fixSaltAndPepper(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        Backend.modifiedImage = Backend.fix_sp_noise(Backend.modifiedImage)
        self.loadImages()

    def showEquHistogram(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        Backend.equalizedHistogram(Backend.modifiedImage)
        self.loadImages()

    def showLapOfGaus(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        plt.close("all")#Close existing plots before creating a new one
        plt.plot(111)
        plt.imshow(Backend.LaplaceOfGaussianAlogrithm(self, Backend.currImage),cmap="gray")
        plt.axis("off")
        plt.show()

    def showLaplace(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        plt.close("all")#Close existing plots before creating a new one
        plt.plot(111)#141)

        plt.imshow(Backend.LaplaceAlogrithm(self, Backend.currImage),cmap="gray")
        plt.axis("off")
        plt.show()


    def showSobelEdge(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        plt.close("all")#Close existing plots before creating a new one
        plt.plot(111)

        plt.imshow(Backend.Sobel_edge_detector(self, Backend.currImage),cmap="gray")
        plt.axis("off")
        plt.show()

    def showSobelAlgorithm(self):
        
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        plt.close("all")#Close existing plots before creating a new one
        plt.plot(111)
        plt.imshow(Backend.SobelAlogrithm(self,Backend.currImage),cmap="gray")
        plt.axis("off")
        plt.show()
        
    #Call functions from backend (End)
        
    #Save Modified Image
    def saveImage(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
        #Open save file dialog
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', QDir.rootPath() , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Save image
            Backend.modifiedImage.save(fileName)

