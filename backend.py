from PIL import Image, ImageQt
from PyQt5 import QtWidgets
from matplotlib import pyplot as plt
import numpy as np
import random
import cv2
from scipy import fft, signal
from scipy.ndimage import rotate

class Backend():
    #Creating a one-pixel image for initializing the currImage
    default_image = True
    mode = 'RGB'
    size = (1, 1)
    color = (0, 0, 0)
    currImage = Image.new(mode, size, color)
    modifiedImage = Image.new(mode, size, color)
    
    image_size = 240#Used for scaling loaded images
    clicks = 0
    clicksData = np.zeros((2, 2))
    
    #Shows a message to inform the user of a problem
    def showMessage(title, message):
        msg = QtWidgets.QMessageBox()
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    #This default message is used at the clicks of all image modification buttons to ask the user for an image
    def noImageSelected():
        Backend.showMessage("Missing Image","No image has been loaded yet. Please select and load an image in order to use this function.")

    #Convert current image to grayscale
    def transformToGray(self):
        self.modifiedImage = self.currImage.convert('L')

    #Make the image usable by PyQt controls
    def imageToQImage(pilImage):
        qImage = ImageQt.ImageQt(pilImage)
        return qImage

    #Convert the image to a numpy array to be usable by scipy
    def imageToSKImage(pilImage):
        skImage = np.array(pilImage)
        return skImage

    #Produce Fourrier Shift
    def get_fft_shift(im):
        im_fft = fft.fft2((im).astype(float))
        return fft.fftshift( im_fft )

    #Ploot an image
    def plot_image(fig, title, img, row, col, cell):
        ax = fig.add_subplot(row, col, cell)
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        ax.set_title(title)

    #Plot Frequency
    def plot_freq(fig, title, freq, row, col, cell, ylim=False):
        ax = fig.add_subplot(row, col, cell)
        log_freq = (20*np.log10( 0.1 + freq))
        log_freq = log_freq.clip(min=0)
        plt.imshow(log_freq.astype(int), cmap=plt.cm.gray)
        ax.set_title(title)
        if ylim == True:
            plt.ylim([log_freq.shape[0]/2+100, log_freq.shape[0]/2-100])
            plt.tight_layout()
        plt.show()

    #Get user click locations for the periodic noise
    def getUserClick(event):        
        if Backend.clicks == 0 or Backend.clicks == 1:
            Backend.clicksData[Backend.clicks, 0] = int(event.xdata)
            Backend.clicksData[Backend.clicks, 1] = int(event.ydata)
            Backend.clicks += 1

        if Backend.clicks == 2:
            Backend.clicks = 0
            im_recovered_fft_shift = np.copy(Backend.im_noisy_fft_shift)

            x1 = Backend.clicksData[0, 0]
            y1 = Backend.clicksData[0, 1]
            x2 = Backend.clicksData[1, 0]
            y2 = Backend.clicksData[1, 1]

            # Remove the periodic noisy as seen in the image
            for i in range(im_recovered_fft_shift.shape[0]):
                for j in range(im_recovered_fft_shift.shape[1]):
                    if i == y1 or i == y2 or j == x1 or j == x2:
                        im_recovered_fft_shift[i][j] = 0

            fig3 = plt.figure()

            # Retrieve original image
            im_fft_restored = fft.ifftshift(im_recovered_fft_shift)
            im_restored = np.real(fft.ifft2(im_fft_restored))
            Backend.plot_image(fig3, 'Recovered Image', im_restored, 1, 2, 1)
            Backend.plot_freq(fig3, 'Recovered Image Spectrum', im_recovered_fft_shift, 1, 2, 2)
            
    
    #Produce Periodic noise (first button)
    def periodic_noise_common(self, pilImage):
        try:
            factor = float(self.periodicText.text())
            if factor > 5 or factor < 0.1:
                raise Exception()
        except:
            Backend.showMessage("Wrong Value", "Periodic noise value must be a float number between 0.1 and 5")
            return

        # Original image
        fig = plt.figure()

        #skImage = Backend.imageToSKImage(pilImage)
        im_mod_arr = np.asarray(pilImage.getdata()).reshape(pilImage.size[1], pilImage.size[0], -1)
        im = np.mean(im_mod_arr, axis=2) / 255
        
        Backend.plot_image(fig, 'Original Image', im, 2, 2, 1)

        # Get original image in frequency domain
        im_fft_shift = Backend.get_fft_shift(im)
        Backend.plot_freq(fig, 'Original Image Spectrum', im_fft_shift, 2, 2, 2)

        
        
        # Add periodic noise to the image
        im_noisy = np.copy(im)
        for n in range(im.shape[1]):
            im_noisy[:, n] += np.cos(factor*np.pi*n)

        Backend.plot_image(fig, 'Image after adding Periodic Noise', im_noisy, 2, 2, 3)

        # Noisy image in frequency domain
        Backend.im_noisy_fft_shift = Backend.get_fft_shift(im_noisy)
        Backend.plot_freq(fig, 'Noisy Image Spectrum', Backend.im_noisy_fft_shift, 2, 2, 4)

        fig2 = plt.figure()
        fft_diff = Backend.im_noisy_fft_shift - im_fft_shift
        Backend.plot_freq(fig2, 'Diff between Noisy and Original Spectrum', fft_diff, 1, 1, 1, True)
        return fig2

    #Produce Periodic noise (second button)
    def periodic2_noise(self, pilImage):
        fig2 = Backend.periodic_noise_common(self, pilImage)
        fig2.canvas.mpl_connect('button_press_event', Backend.getUserClick)

    def periodic_noise(self, pilImage):
        Backend.periodic_noise_common(self, pilImage)
        im_recovered_fft_shift = np.copy(Backend.im_noisy_fft_shift)

        # Remove the periodic noisy as seen in the image
        limit = 1
        print(im_recovered_fft_shift.shape)
        for i in range(im_recovered_fft_shift.shape[0]):
            for j in range(im_recovered_fft_shift.shape[1]):
                if i > im_recovered_fft_shift.shape[0]/2-limit and i < im_recovered_fft_shift.shape[0]/2+limit:
                    im_recovered_fft_shift[i][j] = 0

        fig3 = plt.figure()

        # Retrieve original image
        im_fft_restored = fft.ifftshift(im_recovered_fft_shift)
        im_restored = np.real(fft.ifft2(im_fft_restored))
        Backend.plot_image(fig3, 'Recovered Image', im_restored, 1, 2, 1)
        Backend.plot_freq(fig3, 'Recovered Image Spectrum', im_recovered_fft_shift, 1, 2, 2)


    #Adding Salt and Pepper noise
    def add_sp_noise(pilImage):
        #Convert pillow image to numpy
        img = Backend.imageToSKImage(pilImage)
        # Getting the dimensions of the image
        row , col = img.shape[:2]#Error at :-1
        
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
        median_blur= cv2.medianBlur(Backend.imageToSKImage(pilImage.convert("L")), 3)
        return Image.fromarray(median_blur)

        #takes too long
        #Using median filter to fix salt and pepper noise
        data = Backend.imageToSKImage(pilImage.convert("L"))

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

    #Show equalized histogram and equalized image
    def equalizedHistogram(pilImage):
        plt.close("all")#Close existing plots before creating a new one
        img = Backend.imageToSKImage(pilImage.convert("L"))

        equalized_image = cv2.equalizeHist(img)

        max_range = list(range(1, 257))#1 to 256
        eq_hist, bins = np.histogram(equalized_image.ravel(), bins=max_range)
        fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(15,5))
        ax1.bar(max_range[:-1], eq_hist)#1 to 255 .. hist_bars was defined here
        #The next code does not show well on a plot
        # for bar in hist_bars:
        #     yval = bar.get_height()
        #     if yval > 0:
        #         ax1.text(bar.get_x(), yval + .005, yval)

        #Flipped with origin lower to show y axis starting from the bottom
        ax2.imshow(equalized_image[::-1], cmap=plt.cm.gray, origin='lower')
        fig.tight_layout()
        plt.show()
        

    #Sobel Operator , return the operator, can rotate it by a specific degree
    def SobelOperator(degree=0):
        SOBEL_OPERATOR = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        rotated_operator=rotate(SOBEL_OPERATOR, angle=degree)
        return rotated_operator

    #Sobel Algorithm uses the previous function to get the edges with the degree 
    #Sobel parameters ,Degree and threshold
    def SobelAlogrithm(self, pilImage):
        image = Backend.imageToSKImage(pilImage.convert("L"))
        try:
            threshold = int(self.sobelAlgThreshText.text())
            if threshold > 254 or threshold < -1 or threshold == 0:
                raise Exception()
        except:
            Backend.showMessage("Wrong Value", "Threshold value must either be a number between (1 and 254) or -1")
            return

        try:
            degree = int(self.sobelAlgDegreeText.text())
            if degree > 360 or degree < 0:
                raise Exception()
        except:
            Backend.showMessage("Wrong Value", "Degree value must be a number between 0 and 360")
            return

        new_image = np.zeros(image.shape)    #place holder
        kernel= Backend.SobelOperator(degree)#kernel generation
        new_image = signal.convolve2d(image, kernel, boundary='symm', mode='same')#covloution
        new_image = np.abs(new_image)#absolute value
        new_image = 255 - new_image*(255 / np.max(new_image)) #normalization
        if threshold==-1:
            return new_image.astype(np.uint8)
        else:
            ret,th1 = cv2.threshold(new_image,threshold,255,cv2.THRESH_BINARY) #less than threshold set to 0 otherwise set to 255
            return th1

    #Sobel Edge detection , the dafulat one x and y direction ,you can play with the treshold
    def Sobel_edge_detector(self,pilImage):
        
        image = Backend.imageToSKImage(pilImage.convert("L"))
        try:
            threshold = int(self.sobelText.text())
            if threshold > 254 or threshold < -1 or threshold == 0:
                raise Exception()
        except:
            Backend.showMessage("Wrong Value", "Threshold value must either be a number between (1 and 254) or -1")
            return
            
        #place holders
        new_image1 = np.zeros(image.shape)
        new_image2 = np.zeros(image.shape)
        #generating kernels
        sobel_operator_h=Backend.SobelOperator(0)
        sobel_operator_v=Backend.SobelOperator(90)
        #calclute gradient
        new_image1 = signal.convolve2d(image, sobel_operator_h, boundary='symm', mode='same')
        new_image2 = signal.convolve2d(image, sobel_operator_v, boundary='symm', mode='same')
        #magnitude
        new_image1 = np.sqrt(new_image1*new_image1+new_image2*new_image2)
        #normalization
        new_image1 = 255 - new_image1*(255 / np.max(new_image1))
        if threshold==-1:
            return new_image1.astype(np.uint8)
        else:
            ret,th1 = cv2.threshold(new_image1,threshold,255,cv2.THRESH_BINARY) #less than threshold set to 0 otherwise set to 255
        return th1

    #return the laplace operator , two most recommended filters 
    def LaplaceOperator(operator_type):
        if operator_type == "fourfields":
            laplace_operator = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        elif operator_type == "eightfields":
            laplace_operator = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
        else:
            raise ("type Error")
        return laplace_operator

    #laplace edge detection , you can change the threshold  and the operator type
    def LaplaceAlogrithm(self,pilImage):
        image = Backend.imageToSKImage(pilImage.convert("L"))
        try:
            threshold = int(self.LapThreshText.text())
            if threshold > 254 or threshold < -1 or threshold == 0:
                raise Exception()
        except:
            Backend.showMessage("Wrong Value", "Threshold value must either be a number between (1 and 254) or -1")
            return
        
        operator_type = str(self.LapOpText.currentText()).replace(" ","")

        new_image = np.zeros(image.shape)
        image = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_DEFAULT)
        laplace_operator = Backend.LaplaceOperator(operator_type)
        new_image = signal.convolve2d(image, laplace_operator, mode='same')
        new_image = np.abs(new_image)
        new_image = 255-new_image * (255 / np.max(image))
        
        if threshold==-1:
            return new_image.astype(np.uint8)
        else:
            ret,th1 = cv2.threshold(new_image,threshold,255,cv2.THRESH_BINARY) #less than threshold set to 0 otherwise set to 255
        return th1

    #laplace of gaussian , you can change the smoothing kernel , operator type and threshold 
    def LaplaceOfGaussianAlogrithm(self, pilImage):

        try:
            threshold = int(self.LoGThreshText.text())
            if threshold > 254 or threshold < -1 or threshold == 0:
                raise Exception()
        except:
            Backend.showMessage("Wrong Value", "Threshold value must either be a number between (1 and 254) or -1")
            return
        
        operator_type =str(self.LoGOpText.currentText()).replace(" ","")
        kernel_size = int(self.LoGKerText.currentText())
        

        image = Backend.imageToSKImage(pilImage.convert("L"))
        new_image = np.zeros(image.shape)
        blur = cv2.GaussianBlur(image,(kernel_size,kernel_size),0)
        blur = cv2.copyMakeBorder(blur, 1, 1, 1, 1, cv2.BORDER_DEFAULT)
        laplace_operator = Backend.LaplaceOperator(operator_type)
        new_image = signal.convolve2d(blur, laplace_operator, mode='same')
        new_image=np.abs(new_image)

        new_image = 255-new_image * (255 / np.max(image))
        # print(np.max(new_image))
        if threshold==-1:
            return new_image.astype(np.uint8)
        else:
            ret,th1 = cv2.threshold(new_image,threshold,255,cv2.THRESH_BINARY) #less than threshold set to 0 otherwise set to 255
        return th1
