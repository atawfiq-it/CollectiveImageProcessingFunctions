from PIL import Image, ImageQt
from PyQt5.QtGui import QImage
from matplotlib import pyplot as plt
import numpy as np
import random
import cv2
from scipy import fft, signal
from scipy.ndimage import rotate



class Backend():
    #Creating a one-pixel image for initializing the currImage
    mode = 'RGB'
    size = (1, 1)
    image_size = 240
    color = (0, 0, 0)
    currImage = Image.new(mode, size, color)
    modifiedImage = Image.new(mode, size, color)
    histImage = Image.new(mode, size, color)
    clicks = 0
    clicksData = np.zeros((2, 2));

    def transformToGray(self):
        #Convert current image to grayscale
        self.modifiedImage = self.currImage.convert('L')

    def imgToGray(img):
        imgGray = img.convert('LA')
        return imgGray
    
    def imageToQImage(pilImage):
        qImage = ImageQt.ImageQt(pilImage)
        return qImage

    def imageToSKImage(pilImage):
        skImage = np.array(pilImage)
        return skImage

    def get_fft_shift(im):
        im_fft = fft.fft2((im).astype(float))
        return fft.fftshift( im_fft )

    def plot_image(fig, title, img, row, col, cell):
        ax = fig.add_subplot(row, col, cell)
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        ax.set_title(title)

    def plot_freq(fig, title, freq, row, col, cell):
        ax = fig.add_subplot(row, col, cell)
        plt.imshow( (20*np.log10( 0.1 + freq)).astype(int), cmap=plt.cm.gray)
        ax.set_title(title)

    def onclick(event):        
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
            
    
    def periodic_noise_common(self, pilImage):
        # Original image
        fig = plt.figure()

        skImage = Backend.imageToSKImage(pilImage)
        im = np.mean(skImage, axis=2) / 255
        Backend.plot_image(fig, 'Original Image', im, 2, 2, 1)

        # Get original image in frequency domain
        im_fft_shift = Backend.get_fft_shift(im)
        Backend.plot_freq(fig, 'Original Image Spectrum', im_fft_shift, 2, 2, 2)

        factor = float(self.periodicText.text())

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
        Backend.plot_freq(fig2, 'Diff between Noisy and Original Spectrum', fft_diff, 1, 1, 1)

        fig2.canvas.mpl_connect('button_press_event', Backend.onclick)

    def periodic2_noise(self, pilImage):
        Backend.periodic_noise_common(self, pilImage)

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


    def add_sp_noise(pilImage):
    #Adding Salt and Pepper

        #Convert pillow image to open-cv
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

    def fourierTransform(pilImage):
        image1 = Backend.imageToSKImage(pilImage.convert("L"))
        image1_spectrum = np.fft.fft2(image1)
        image1_spectrum_centered=np.fft.ifftshift(image1_spectrum)
        
        # src = cv2.imread("C:/Users/User/Pictures/L424502.jpg")
        #plt.figure(figsize=(24, 16), constrained_layout=False)
        # image1 = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        # plt.subplot(121), plt.imshow(image1), plt.title("Original Image")

        plt.subplot(111), plt.imshow(np.log(1+np.abs(image1_spectrum_centered)), "gray"), plt.title("Spectrum")
        plt.show()

    def equalizedHistogram(pilImage):
        img = Backend.imageToSKImage(pilImage.convert("L"))


        equalized_image = cv2.equalizeHist(img)
        #plt.figure(figsize=(20, 16), constrained_layout=False)
        #plt.subplot(1,2,1),plt.hist(equalized_image.ravel(),bins=100),plt.title("Equalized histogram")
        
        
        #plt.subplot(1,2,2),plt.imshow(equalized_image,"gray", aspect='auto'),plt.title("Equalized Image")

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
    def SobelAlogrithm(pilImage,degree=0,threshold=-1):
        
        image = Backend.imageToSKImage(pilImage.convert("L"))
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
    def Sobel_edge_detector(pilImage,threshold=-1):
        
        image = Backend.imageToSKImage(pilImage.convert("L"))
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
    def LaplaceAlogrithm(pilImage, operator_type="eightfields",threshold=-1):
        image = Backend.imageToSKImage(pilImage.convert("L"))
        new_image = np.zeros(image.shape)
        image = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_DEFAULT)
        laplace_operator = Backend.LaplaceOperator(operator_type)
        new_image = signal.convolve2d(image, laplace_operator, mode='same')
        new_image=np.abs(new_image)
        new_image = 255-new_image * (255 / np.max(image))
        if threshold==-1:
            return new_image.astype(np.uint8)
        else:
            ret,th1 = cv2.threshold(new_image,threshold,255,cv2.THRESH_BINARY) #less than threshold set to 0 otherwise set to 255
        return th1

    #laplace of gaussian , you can change the smoothing kernel , operator type and threshold 
    def LaplaceOfGaussianAlogrithm(pilImage,operator_type="eightfields",kernel_size=3,threshold=-1):
        if kernel_size%2==0:
            print("kernel size must be odd number")
            return 

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
