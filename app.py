import PIL
from PyQt5 import QtCore
import numpy as np
from gui import MainUI
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from backend import Backend
from PIL import Image, ImageQt
import matplotlib.pyplot as plt

#Main Window Class
class ImageProcessingWindow(QDialog, MainUI):
    def __init__(self, parent=None):
        super(ImageProcessingWindow, self).__init__(parent)
        
        #Getting controls for both main window and extra window from the gui.py file
        self.setupGUI(self)
        self.setLayout(self.mainLayout)
        #Disable question mark on top, enable minimize, maximize, and close buttons
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | 
        QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint| QtCore.Qt.WindowMinimizeButtonHint)


    

    

    def loadImages(self):
        #Converting image to qImage and showing it in the image control
        qImage1 = Backend.imageToQImage(Backend.currImage)
        self.labelOriginalImage.setPixmap(QPixmap.fromImage(qImage1).scaled(Backend.image_size, Backend.image_size))
        self.labelOriginalImage.setScaledContents(True)

        qImage2 = Backend.imageToQImage(Backend.modifiedImage)
        self.labelModifiedImage.setPixmap(QPixmap.fromImage(qImage2).scaled(Backend.image_size, Backend.image_size))
        self.labelModifiedImage.setScaledContents(True)

        #Show plot images after an image is loaded
        self.showPlot()
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

        
    def getImagePath(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', QDir.rootPath() , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Open image in the original QPixMap
            self.styleTextBoxPath.setText(fileName)
            #Open image if selected through browse directly
            self.getImageFile()
            

    def getImageFile(self):

        #If the filename is not empty
        if self.styleTextBoxPath.text():
            #Reading into an image object and showing it in the image control
            try:
                Backend.currImage = Image.open(self.styleTextBoxPath.text()).convert("L")
                #Copy original image to the modified
                self.toOriginal(True)#Skip Check of existing image
            except FileNotFoundError:
                Backend.showMessage("Incorrect Path","The provided file path is not correct. Please provide a valid file path.")
            except PIL.UnidentifiedImageError:
                Backend.showMessage("Incorrect Type","The provided file can not be interpreted as a valid image. Please provide a valid path to an image file.")
        else:
            Backend.showMessage("Empty Path","Kindly fill in the file path or use the Browse button to select a file.")

            
    def toPeriodic(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        Backend.periodic_noise(self, Backend.currImage)

        #set image control to the converted image
        self.loadImages()

    def toPeriodic2(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        Backend.periodic2_noise(self, Backend.currImage)

        #set image control to the converted image
        self.loadImages()



    def toOriginal(self, skip=False):
        if Backend.default_image == True and skip == False:
            Backend.noImageSelected()
            return

        Backend.modifiedImage = Backend.currImage.copy()
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

        grayArray = np.array(Backend.imgToGray(Backend.currImage))
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

    def showFourier(self):
        Backend.fourierTransform(Backend.modifiedImage)

    def showEquHistogram(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        Backend.equalizedHistogram(Backend.modifiedImage)

    def showLapOfGaus(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        plt.subplot(111)
        #plt.title("loG 3x3")
        plt.imshow(Backend.LaplaceOfGaussianAlogrithm(self, Backend.currImage),cmap="gray")
        plt.axis("off")
        # plt.subplot(132)
        # plt.title("loG 5x5")
        # plt.imshow(Backend.LaplaceOfGaussianAlogrithm(Backend.currImage,operator_type="eightfields",kernel_size=5),cmap="gray")
        # plt.axis("off")
        # plt.subplot(133)

        # plt.title("loG 7x7")
        # plt.imshow(Backend.LaplaceOfGaussianAlogrithm(Backend.currImage,operator_type="eightfields",kernel_size=17),cmap="gray")
        # plt.axis("off")
        plt.show()

    def showLaplace(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        plt.subplot(111)#141)
        #plt.title("thresh = " + str(thresholdVal))

        plt.imshow(Backend.LaplaceAlogrithm(self, Backend.currImage),cmap="gray")#,operator_type="eightfields",threshold=thresholdVal),cmap="gray")
        plt.axis("off")

        # plt.subplot(142)

        # plt.title("thresh =127")

        # plt.imshow(Backend.LaplaceAlogrithm(Backend.currImage,operator_type="eightfields",threshold=127),cmap="gray")
        # plt.axis("off")

        # plt.subplot(143)

        # plt.title("thresh =200")

        # plt.imshow(Backend.LaplaceAlogrithm(Backend.currImage,operator_type="eightfields",threshold=200),cmap="gray")
        # plt.axis("off")
        # plt.subplot(144)

        # plt.title("defualt")

        # plt.imshow(Backend.LaplaceAlogrithm(Backend.currImage,operator_type="eightfields"),cmap="gray")
        # plt.axis("off")

        plt.show()


    def showSobelEdge(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        plt.subplot(111)

        #plt.title("thresh=10")

        plt.imshow(Backend.Sobel_edge_detector(self, Backend.currImage),cmap="gray")
        plt.axis("off")
        # plt.subplot(142)
        # plt.title("thresh=127")
        # plt.imshow(Backend.Sobel_edge_detector(Backend.currImage,threshold=127),cmap="gray")

        # plt.axis("off")

        # plt.subplot(143)
        # plt.title("thresh=200")

        # plt.imshow(Backend.Sobel_edge_detector(Backend.currImage,threshold=200),cmap="gray")
        # plt.axis("off")

        # plt.subplot(144)
        # plt.title("defualt")

        # plt.imshow(Backend.Sobel_edge_detector(Backend.currImage),cmap="gray")
        # plt.axis("off")


        plt.show()

    def showSobelAlgorithm(self):
        
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        plt.subplot(111)

        #plt.title("degree=0")

        plt.imshow(Backend.SobelAlogrithm(self,Backend.currImage),cmap="gray")
        plt.axis("off")
        # plt.subplot(142)
        # plt.title("degree=45")
        # plt.imshow(Backend.SobelAlogrithm(Backend.currImage,degree=45),cmap="gray")

        # plt.axis("off")

        # plt.subplot(143)
        # plt.title("degree=90")

        # plt.imshow(Backend.SobelAlogrithm(Backend.currImage,degree=90),cmap="gray")
        # plt.axis("off")

        # plt.subplot(144)
        # plt.title("degree=135")

        # plt.imshow(Backend.SobelAlogrithm(Backend.currImage,degree=135),cmap="gray")
        # plt.axis("off")


        plt.show()
    
        

    def saveImage(self):
        if Backend.default_image == True:
            Backend.noImageSelected()
            return
            
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', QDir.rootPath() , '*.png *.jpg *.jpeg')

        #If the filename is not empty
        if fileName:
            #Save image
            Backend.modifiedImage.save(fileName)

