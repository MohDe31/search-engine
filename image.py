import math
import numpy as np
from PIL import Image
import cv2

def rgb_to_ycrcb(img: np.ndarray):
    axe = np.array([
        [.299,  .499813,    -.168935],
        [.587,  -.418531,   -.331665],
        [.114,  -.081282,   .50059  ]
    ])

    result = (np.matmul(img, axe) + [0, 128, 128]).astype("uint8")

    return result
# 0 1 8 16 9 2 3 10 17 24 32 25 18 11 4 5 12 19 26 33 40 48 41 34
def zigzag_scan(img, dw, dh, p, q):
    i = 64
    x, y = 0, 0

    img = []
    for i in range(8):
        img.append([])
        for j in range(8):
            img[-1].append(i*8+j)

    img = np.array(img)

    yy =  1
    xx = -1

    i = 63

    print(img)
    while i:
        print(end=f"{img[x, y]} ")

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
        
    print(img[x, y])


def dct88(block):
    w, *h = block.shape
    h = h[0]

    yBlock = np.zeros((w, h))
    crBlock = np.zeros((w, h))
    cbBlock = np.zeros((w, h))

    for u in range(8):
        for v in range(8):
            sum_y = 0
            sum_cr = 0
            sum_cb = 0
            
            for x in range(8):
                for y in range(8):
                    val = math.cos(((2.0*x+1)*u*math.pi)/16.0)*math.cos(((2.0*y+1)*v*math.pi)/16.0)
                    
                    sum_y = sum_y + block[x, y, 0] * val
                    sum_cr = sum_cr + block[x, y, 1] * val
                    sum_cb = sum_cb + block[x, y, 2] * val

        cu = 1/math.sqrt(2) if u == 0 else 1
        cv = 1/math.sqrt(2) if v == 0 else 1

        yBlock[u, v] = 1/4*cu*cv*sum_y
        crBlock[u, v] = 1/4*cu*cv*sum_cr
        cbBlock[u, v] = 1/4*cu*cv*sum_cb

    return yBlock, crBlock, cbBlock

def IDCT(img):
    w, *h = img.shape
    
    h = h[0]

    div_w = w // 8# w // 8 if w // 8 != w / 8 else math.floor((w-1) / 8)
    div_h = h // 8# h // 8 if h // 8 != h / 8 else math.floor((h-1) / 8)

    img = img[0 : div_w * 8, 0 : div_h * 8]

    ORIGINAL_IMAGE = np.zeros((w, h))

    for i in range(div_w):
        for j in range(div_h):
            current_block = img[i*8 : (i+1)*8, j*8 : (j+1)*8]

            for u in range(8):
                for v in range(8):

                    sum_ = 0

                    for x in range(8):
                        for y in range(8):
                            val = math.cos(((2*x+1)*u*math.pi)/16.0)*math.cos(((2*y+1)*v*math.pi)/16.0)
                            cu = 1/math.sqrt(2) if x == 0 else 1
                            cv = 1/math.sqrt(2) if y == 0 else 1
                            
                            sum_ += current_block[x, y] * val * cu * cv
                    
                    ORIGINAL_IMAGE [i*8+u, j*8+v] = sum_ / 4
            
    Image.fromarray(ORIGINAL_IMAGE + 128).show()

    return ORIGINAL_IMAGE
    

def DCT(img):
    w, *h = img.shape
    
    h = h[0]

    div_w = w // 8# w // 8 if w // 8 != w / 8 else math.floor((w-1) / 8)
    div_h = h // 8# h // 8 if h // 8 != h / 8 else math.floor((h-1) / 8)

    img = img[0 : div_w * 8, 0 : div_h * 8]

    Image.fromarray(img[:,:,0]).show()
    img = rgb_to_ycrcb(img) - 128


    DCTY = np.zeros((w, h))
    DCTCb= np.zeros((w, h))
    DCTCr= np.zeros((w, h))


    for i in range(div_w):
        for j in range(div_h):
            current_block = img[i*8 : (i+1)*8, j*8 : (j+1)*8]

            for u in range(8):
                for v in range(8):
                    cu = 1/math.sqrt(2) if u == 0 else 1
                    cv = 1/math.sqrt(2) if v == 0 else 1

                    sum_y = 0

                    for x in range(8):
                        for y in range(8):
                            val = math.cos(((2.0*x+1)*u*math.pi)/16.0)*math.cos(((2.0*y+1)*v*math.pi)/16.0)
                            
                            sum_y += current_block[x, y, 0] * val
                
                    DCTY[i*8 + u, j*8 + v] = sum_y * (cu * cv) / 4
            
    print(DCTY)
    Image.fromarray(DCTY).show()

    return DCTY
    #zigzag_scan(img, div_w, div_h, 0, 0)

def dct_(tga, data, xpos, ypos):
    u,v,x,y = 0, 0, 0, 0

    for v in range(8):
        for u in range(8):
            z = 0
            Cu = 1/math.sqrt(2) if u == 0 else 1
            Cv = 1/math.sqrt(2) if v == 0 else 1

            for y in range(8):
                for x in range(8):
                    q = 0
                    s = tga[x + xpos, y + ypos]
                    q = s * math.cos((2*x+1) * u * math.pi/16.0) * math.cos((2*y+1) * v * math.pi/16.0)

                    z += q
                
            data[v][u] = 0.25 * Cu * Cv * z

def quanitize(data):
    for i in range(8):
        for j in range(8):
            if i > 3 or j > 3: data[i, j] = 0

def idct_(tga, data, xpos, ypos):
    for y in range(8):
        for x in range(8):
            z = 0

            for v in range(8):
                for u in range(8):
                    Cu = 1/math.sqrt(2) if u == 0 else 1
                    Cv = 1/math.sqrt(2) if v == 0 else 1

                    S = data[v, u]

                    q = Cu * Cv * S * math.cos((2*x+1) * u * math.pi/16.0) * math.cos((2*y+1) * v * math.pi/16.0)

                    z+=q
            z /= 4
            
            if (z > 255.0): z = 255.0
            if (z < 0): z = 0.0

            tga[x+xpos, y+ypos] = int(z)


img = list(np.array(Image.open("download.jfif").resize((100, 100))))
for row in img:
    print(row)
exit(0)

img = np.array(Image.open("download.jfif").resize((100, 100)))

w, *h = img.shape
    
h = h[0]

div_w = w // 8# w // 8 if w // 8 != w / 8 else math.floor((w-1) / 8)
div_h = h // 8# h // 8 if h // 8 != h / 8 else math.floor((h-1) / 8)

img = img[0 : div_w * 8, 0 : div_h * 8]

img = (rgb_to_ycrcb(img))[:,:,0]
Image.fromarray(img).show()

data = np.zeros((8, 8))
for j in range(div_w):
    for i in range(div_h):
        dct_(img, data, i*8, j*8)
        #img[i*8:(i+1)*8,j*8:(j+1)*8] = data
        quanitize(data)
        idct_(img, data, i*8, j*8)


Image.fromarray(img.astype("uint8")).show()
