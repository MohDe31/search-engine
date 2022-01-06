from ctypes import *
import ctypes
import numpy as np
import cv2

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

def freeman(img):
    img = process_img(img).astype("uint8")

    return ''.join(map(str,max(get_chaine(img), key=len)[2:]))

def compare(img1, img2):
    c1 = freeman(img1)
    c2 = freeman(img2)

    dist = np.array([(c1.count(i) - c2.count(i))**2 for i in '01234567']).sum()**.5
    return dist

def compare_ci(c1, img):
    c2 = freeman(img)

    dist = np.array([(c1.count(i) - c2.count(i))**2 for i in '01234567']).sum()**.5
    return dist
