from PIL import Image, ImageQt
from PyQt5.QtGui import QImage
from matplotlib import pyplot as plt
import numpy as np
import random
import cv2
from scipy import fft


class Variables():
    #Creating a one-pixel image for initializing the currImage
    mode = 'RGB'
    size = (1, 1)
    image_size = 240
    color = (0, 0, 0)
    currImage = Image.new(mode, size, color)
    modifiedImage = Image.new(mode, size, color)
    histImage = Image.new(mode, size, color)

    def transformToGray(self):
        #Convert current image to grayscale
        self.modifiedImage = self.currImage.convert('L')

    def imgToGray(img):
        imgGray = img.convert('LA')
        return imgGray
    
    def imageToQImage(pilImage):
        qImage = ImageQt.ImageQt(pilImage)
        return qImage

    def get_fft_shift(im):
        im_fft = fft.fft2((im).astype(float))
        return fft.fftshift( im_fft )

    def add_sp_noise(pilImage):
    #Adding Salt and Pepper

        #Convert pillow image to open-cv
        img = np.array(pilImage)
        # Getting the dimensions of the image
        row , col = img.shape[:-1]
        
        # Randomly pick some pixels in the
        # image for coloring them white
        # Pick a random number between 300 and 10000
        number_of_pixels = random.randint(300, 10000)
        for i in range(number_of_pixels):
            
            # Pick a random y coordinate
            y_coord=random.randint(0, row - 1)
            
            # Pick a random x coordinate
            x_coord=random.randint(0, col - 1)
            
            # Color that pixel to white
            img[y_coord][x_coord] = 255
            
        # Randomly pick some pixels in
        # the image for coloring them black
        # Pick a random number between 300 and 10000
        number_of_pixels = random.randint(300 , 10000)
        for i in range(number_of_pixels):
            
            # Pick a random y coordinate
            y_coord=random.randint(0, row - 1)
            
            # Pick a random x coordinate
            x_coord=random.randint(0, col - 1)
            
            # Color that pixel to black
            img[y_coord][x_coord] = 0
        
        imgResult = Image.fromarray(img)
        return imgResult
    
    def fix_sp_noise(pilImage, filter_size=3):
    #Using median filter to fix salt and pepper noise

        data = np.array(pilImage.convert("L"))

        temp = []
        indexer = filter_size // 2
        data_final = []
        data_final = np.zeros((len(data),len(data[0])))
        for i in range(len(data)):

            for j in range(len(data[0])):

                for z in range(filter_size):
                    if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                        for c in range(filter_size):
                            temp.append(0)
                    else:
                        if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                            temp.append(0)
                        else:
                            for k in range(filter_size):
                                temp.append(data[i + z - indexer][j + k - indexer])

                temp.sort()
                data_final[i][j] = temp[len(temp) // 2]
                temp = []

                imgResult = Image.fromarray(data_final)
        return imgResult

    def fourierTransform(pilImage):
        image1 = np.array(pilImage.convert("L"))
        image1_spectrum = np.fft.fft2(image1)
        image1_spectrum_centered=np.fft.ifftshift(image1_spectrum)
        
        # src = cv2.imread("C:/Users/User/Pictures/L424502.jpg")
        #plt.figure(figsize=(24, 16), constrained_layout=False)
        # image1 = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        # plt.subplot(121), plt.imshow(image1), plt.title("Original Image")

        plt.subplot(111), plt.imshow(np.log(1+np.abs(image1_spectrum_centered)), "gray"), plt.title("Spectrum")
        plt.show()

    def equalizedHistogram(pilImage):
        img = np.array(pilImage.convert("L"))
        equalized_image = cv2.equalizeHist(img)
        #plt.figure(figsize=(20, 16), constrained_layout=False)
        plt.subplot(121),plt.hist(equalized_image.flatten(),256,[0,256], color = 'b'),plt.xlim([0,256]),plt.title("Equalized histogram")
        plt.subplot(122),plt.imshow(equalized_image,"gray"),plt.title("Equalized Image")
        plt.show()