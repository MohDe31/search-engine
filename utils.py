import numpy as np
import cv2

def isGray(a, threshold = 5):
    avg = a.sum(axis=2)/3

    rv = a[..., 0] - avg
    gv = a[..., 1] - avg
    bv = a[..., 2] - avg

    varr = np.abs(np.dstack((rv, gv, bv)))

    size = eval('*'.join(map(str,a.shape[:2])))

    return (varr.sum(axis=2)/3).sum()/size < threshold