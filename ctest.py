from ctypes import *
import ctypes
import numpy as np
from PIL import Image
import cv2
from numpy.ctypeslib import as_ctypes
libCalc = CDLL("./utils/libdct.so")

def Naif_Detector(image):
    vertical = abs(image[:, 0: -1] - image[:, 1:])
    horizontal = abs(image[0: -1, :] - image[1:, :])
    contour = np.sqrt(vertical[:-1,:]**2 + horizontal[:,:-1]**2)
    np.putmask(contour, contour > 255, 255)
    return contour

def process_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    binary = (blur < 127) * 255
    return Naif_Detector(binary)

def get_chaine(img):

    # Create an image pointer
    img_c  = img.astype(np.int32).ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

    # Create a pointer
    freeman_c= np.zeros((int(1e9),), dtype=np.int16).ctypes.data_as(ctypes.POINTER(ctypes.c_int16))

    h, w = img.shape

    size = libCalc.freeman(img_c, freeman_c, w, h, 0)

    chaine = np.ctypeslib.as_array(freeman_c, (size,)).astype(np.int16)
    
    return [*map(lambda x:[*map(int,x.strip().split()),],' '.join(map(str,chaine)).split('-1')),]

def compare(img1, img2):
    img1 = process_img(img1).astype("uint8")
    img2 = process_img(img2).astype("uint8")

    shape1 = eval('*'.join(map(str,img1.shape[:2])))
    shape2 = eval('*'.join(map(str,img2.shape[:2])))
    
    if shape1 < shape2: img2 = cv2.resize(img2, img1.shape)
    else: img1 = cv2.resize(img1, img2.shape)

    c1 = get_chaine(img1)
    c2 = get_chaine(img2)

    c1 = ''.join(map(str,max(c1, key=len)[2:]))
    c2 = ''.join(map(str,max(c2, key=len)[2:]))

    dist = np.array([(c1.count(i) - c2.count(i))**2 for i in '01234567']).sum()**.5
    return dist