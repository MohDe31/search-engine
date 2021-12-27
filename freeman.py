from PIL import Image
import numpy as np

image = np.array(Image.open('gear.jpg'))
image[image <  100] = 0
image[image >= 100] = 255


start = [*zip(*np.where(image == 255)),][0]


#3 2 1
#4 X 0
#5 6 7

direction = 4

dir_idx = [* zip(
    [1, 1, 0, -1, -1, -1, 0, 1],
    [0, 1, 1, 1, 0, -1, -1, -1]
) ,]

contour = []
start_pos = start

def start_chain(img, idx, direction):
    global dir_idx, contour, start_pos

    print(idx)

    x, y = idx
    
    loop_start_dir = direction

    while(True):
        xd, yd = dir_idx[direction]
        if (img[x+xd, y+yd]):
            sx, sy = start_pos
            if x+xd == sx and y+yd == sy:
                return
            
            contour += [direction]

            start_chain(img, (x+xd, y+yd), (direction-5)%8)
            return
        
        else:
            direction = (direction - 1) % 8
            if direction == loop_start_dir:
                return


start_chain(image, start, direction)



def build_contour(idx, contour, img):
    global dir_idx
    x, y = idx

    w, h = img.shape

    arr = np.zeros((w, h))

    for dir in contour:
        arr[x, y] = 255
        nx, ny = dir_idx[dir]
        x += nx
        y += ny
        
    Image.fromarray(arr.astype("uint8")).save("image.png")

build_contour(start_pos, contour, image)

