# -*- coding: utf-8 -*-
"""
Created on Fri May 14 01:42:02 2021

@author: akamel
"""

from scipy import fft
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread

def get_fft_shift(im):
    im_fft = fft.fft2((im).astype(float))
    return fft.fftshift( im_fft )

def plot_image(cell, im):
    plt.subplot(4,3,cell), plt.imshow(im, cmap='gray'), plt.axis('off')

def plot_freq(cell, freq):
    plt.subplot(4,3,cell), plt.imshow( (20*np.log10( 0.1 + freq)).astype(int), cmap=plt.cm.gray)

# Original image
plt.figure(figsize=(15,10))
im = np.mean(imread("parrot.PNG"), axis=2) / 255
print(im.shape)
plot_image(1, im)
plt.title('Original Image')

# Get original image in frequency domain
im_fft_shift = get_fft_shift(im)
plot_freq(3, im_fft_shift)
plt.title('Original Image Spectrum')

# Add periodic noise to the image
im_noisy = np.copy(im)
for n in range(im.shape[1]):
    im_noisy[:, n] += np.cos(0.1*np.pi*n)
    
plot_image(4, im_noisy)
plt.title('Image after adding Periodic Noise')

# Noisy image in frequency domain
im_noisy_fft_shift = get_fft_shift(im_noisy)
plot_freq(6, im_noisy_fft_shift)
plt.title('Noisy Image Spectrum')

plot_freq(8, im_noisy_fft_shift - im_fft_shift)
plt.title('Diff between Noisy and Original Spectrum')

im_recovered_fft_shift = np.copy(im_noisy_fft_shift)

# Remove the periodic noisy as seen in the image
limit = 1
print(im_recovered_fft_shift.shape)
for i in range(im_recovered_fft_shift.shape[0]):
    for j in range(im_recovered_fft_shift.shape[1]):
        if i > im_recovered_fft_shift.shape[0]/2-limit and i < im_recovered_fft_shift.shape[0]/2+limit:
            im_recovered_fft_shift[i][j] = 0

# Retrieve original image
im_fft_restored = fft.ifftshift(im_recovered_fft_shift)
im_restored = np.real(fft.ifft2(im_fft_restored))
plot_image(10, im_restored)
plt.title('Recovered Image')

plot_freq(12, im_recovered_fft_shift)
plt.title('Recovered Image Spectrum')

plt.tight_layout()
plt.show()
