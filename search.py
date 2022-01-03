from sqlite3.dbapi2 import Connection, Cursor, connect
from bs4 import BeautifulSoup
from threading import Thread
from bs4.element import Tag
from io import BytesIO
from PIL import Image

import numpy as np
import requests
import sqlite3
import base64
import cv2
import os

from freeman import compare, compare_ci, freeman
from image import DCT
from utils import isGray

def save_urls(link, images): 
    db = sqlite3.connect('database.db')
    curr = db.cursor()

    for image in images:
        name = image['name']
        link = image['link']
        url = image['src']
        
        b64 = url_tob64(url).decode('utf-8')
        if db:
            curr.execute(f'INSERT INTO images (website, file_url, file_name, b64) VALUES("{link}", "{url}", "{name}", "{b64}");')
    
    db.commit()
    db.close()
    print("DONE!!")

def url_tob64(url):
    img = requests.get(url)

    if img.status_code == 200:
        return base64.b64encode(img.content)

    return None

def b64_to_image(b64):
    im_bytes = base64.b64decode(b64)
    im_file  = BytesIO(im_bytes)
    return cv2.cvtColor(np.array(Image.open(im_file)), cv2.COLOR_RGB2BGR)

def searchForImage(value: str):
    img = b64_to_image(value)
    
    assets_folder = os.path.join(os.getcwd(), "assets")

    if isGray(img):
        print("FREEMAN")
        img_freeman = freeman(img)
        images = []
        for filename in os.listdir(assets_folder):
            file_path = os.path.join(assets_folder, filename)
            test_img = cv2.imread(file_path)

            dist = compare_ci(img_freeman, test_img)

            print(file_path, dist)

            if dist <= 110:
                with open(file_path, 'rb') as f:
                    b64 = base64.b64encode(f.read())
                    images.append({'src': str(b64)[2:-1], 'type': 'B64', 'name': filename, 'dist': dist})
                    
        return sorted(images, key=lambda x:x['dist'])
    else:
        print("DCT")
        y1, cb1, cr1 = DCT(img)

        images = []
        for filename in os.listdir(assets_folder):
            file_path = os.path.join(assets_folder, filename)
            print(file_path)
            test_img = cv2.imread(file_path)

            y2, cb2, cr2 = DCT(test_img)
            
            dist = ((((y1-y2)**2).sum())**.5) + ((((cb1-cb2)**2).sum())**.5) + ((((cr1-cr2)**2).sum())**.5)
            print(dist)
            if dist <= 585:
                with open(file_path, 'rb') as f:
                    b64 = base64.b64encode(f.read())
                    images.append({'src': str(b64)[2:-1], 'type': 'B64', 'name': filename, 'dist': dist})
                    
        return sorted(images, key=lambda x:x['dist'])

def searchFor(value: str):
    db_connection: Connection = sqlite3.connect('database.db')

    curr: Cursor = db_connection.cursor()

    worldwildlife =      'https://www.worldwildlife.org/species/elephant'
    britannica    =   'https://www.britannica.com/animal/elephant-mammal'
    thespruce     = 'https://www.thespruce.com/pictures-of-ducks-4121960'

    URLs = [worldwildlife, britannica, thespruce]

    images = curr.execute('SELECT * FROM images;').fetchall()

    output = []
    for url in URLs:
        _cout   = crawlInWeb(value, url)
        _cimage = [*map(lambda x:x[2], images),]

        for val in _cout:
            try:
                idx = _cimage.index(val['src'])

                val['type'] = 'B64'
                val['src' ] = images[idx][4]

            except: continue # Value not found

        output += _cout



    db_connection.close()
    Thread(None, target=lambda: save_urls(url, output)).start()
    return output



def img_filter_func(x: str):
    SUPPORTED_FILES = ['.png', '.jpg', '.jpeg', '.gif']

    return any(map(lambda y:x.endswith(y), SUPPORTED_FILES))

def get_images_names(link: str):
    rev_link = link[::-1]
    dot_ = len(link) - rev_link.find('.') - 1

    slash = len(link) - rev_link.find('/')

    return link[slash: dot_]    
    


def crawlInWeb(value: str, url: str):
    value = value.lower()

    result = requests.get(url)

    if(result.status_code == 200):
        soup = BeautifulSoup(result.text)

        print('|||||||||||||||||||||||')
        
        title = soup.find('title').text.lower()

        links = depthSearch(soup.find('body'))

        images = [* filter(img_filter_func, links) ,]
        
        #TODO DB STUFF

        names  = [*map(get_images_names, images),]

        i_n = [* zip(images, names) ,]

        if value in title:
            return [* map(lambda x:{
                "link": url,
                "src": x[0],
                "name": x[1],
                "type": "URL"
            }, i_n)]

        return []



def depthSearch(tag: Tag):
    images = []

    while tag:
        src = tag.get('src')

        if src: images.append(src)

        tag = tag.find_next()

    return images
