import math
import numpy as np
from PIL import Image

Q = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
], dtype=np.float16)


def rgb_to_ycrcb(img: np.ndarray):
    axe = np.array([
        [.299,  .499813,    -.168935],
        [.587,  -.418531,   -.331665],
        [.114,  -.081282,   .50059  ]
    ])

    result = (np.matmul(img, axe) + [0, 128, 128]).astype("uint8")

    return result
# 0 1 8 16 9 2 3 10 17 24 32 25 18 11 4 5 12 19 26 33 40 48 41 34
def zigzag_scan(dct_mat):
    i = 64
    x, y = 0, 0

    output = np.zeros((3, 64))
    index = 0

    yy =  1
    xx = -1

    i = 63
    while i:
        output[0, index] = dct_mat[x, y, 0]
        output[1, index] = dct_mat[x, y, 1]
        output[2, index] = dct_mat[x, y, 2]

        if yy + y < 0:
            yy = 0
        
        if xx + x < 0:
            xx = 0

        if i <= 28:
            if yy + y > 7:
                yy =  0
                xx = 1
            
            if xx + x > 7:
                xx =  0
                yy = 1

            
        x+=xx
        y+=yy
        

        if not yy:
            yy = -1 if 1 + y > 7 else 1
            xx = -xx if i > 28 else xx

        if not xx:
            xx = -1 if 1 + x > 7 else 1
            yy = -yy if i > 28 else yy
            
        i -= 1
        index += 1
        
    output[0, index] = dct_mat[x, y, 0]
    output[1, index] = dct_mat[x, y, 1]
    output[2, index] = dct_mat[x, y, 2]


    return output


def DCT(img):
    w, h = img.shape[:2]
    
    dW, dH = w // 8, h // 8

    img = rgb_to_ycrcb(img[:dW*8,: dH*8])

    w, h = img.shape[:2]
    #img = img[:dW*8,: dH*8]

    dct = np.zeros((8, 8, 3))

    for i in range(8):
        i_pos, i_pos_next = i * dW, (i+1) * dW
        for j in range(8):
            j_pos, j_pos_next = j * dH, (j+1) * dH
            img[i_pos: i_pos_next, j_pos: j_pos_next] = img[i_pos: i_pos_next, j_pos: j_pos_next].mean(axis=0).mean(axis=0)
    
    img -= 128

    xs, ys = np.where(img[...,0])
    xs = xs.reshape((w, h))
    ys = ys.reshape((w, h))


    for p, i in enumerate(range(0, w, dW)):
        ap = 1 / (w**.5) if p == 0 else (2/w)**.5
        for q, j in enumerate(range(0, w, dH)):
            aq = 1 / (h**.5) if q == 0 else (2/h)**.5

            block = img[i:i+dW,j:j+dH]

            cosx = np.cos(((2*xs[i:i+dW,j:j+dH]+1) * math.pi * p) / (2 * w))
            cosy = np.cos(((2*ys[i:i+dW,j:j+dH]+1) * math.pi * q) / (2 * h))

            dct[p, q, 0] = (ap * aq * np.sum(cosx * cosy * block[..., 0])) / Q[p, q]
            dct[p, q, 1] = (ap * aq * np.sum(cosx * cosy * block[..., 1])) / Q[p, q]
            dct[p, q, 2] = (ap * aq * np.sum(cosx * cosy * block[..., 2])) / Q[p, q]

    return zigzag_scan(dct)
    


img1 = np.array(Image.open("mount.jpg"))
img2 = np.array(Image.open("mount2.jpg"))

y1, cb1, cr1 = DCT(img1)
y2, cb2, cr2 = DCT(img2)

D = ((((y1-y2)**2).sum())**.5) + ((((cb1-cb2)**2).sum())**.5) + ((((cr1-cr2)**2).sum())**.5)

print(D)