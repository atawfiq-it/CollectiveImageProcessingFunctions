#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 01:06:04 2021

@author: user
"""

from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

im = imread("images/403px-Android_robot.png") [:,:,:3]
t = np.mean(im, axis=2) / 255

m = len(t)
n = len(t[0])
t_1 = np.copy(t)
for i in range(m):
    for j in range(n):
        t_1[i, j] += np.cos(0.1*np.pi*j)

plt.figure(figsize=(15,10))
plt.subplot(3,1,1), plt.imshow(im), plt.axis('off')
plt.subplot(3,1,2), plt.imshow(t, cmap='gray'), plt.axis('off')
plt.subplot(3,1,3), plt.imshow(t_1, cmap='gray'), plt.axis('off')
plt.show()
