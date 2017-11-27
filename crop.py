#!/usr/bin/env python

from PIL import Image
import os,string
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

dir_name = r'test/'

dir_ = os.listdir(dir_name)

def cut_img(img_item):

    c_w=232
    c_h=140

    if not os.path.exists(dir_name+'small'):
        os.makedirs(dir_name+'small')

    # if os.path.exists(dir_name+'small/'+img_item):
    #     return True

    im = Image.open(dir_name+img_item)
    im = im.convert('RGB')

    w,h = im.size

    if( (w/h) < (c_w/c_h) ):

        print(c_w / w)
        true_height = (c_w / w)*h
        print(true_height)

        exit()

        im.thumbnail((true_height, true_height), Image.ANTIALIAS)
        im.save(dir_name + 'small/' + img_item, 'JPEG', quality=100)
        exit()

        img = Image.open(dir_name + 'small/'+img_item)

        w1, h1 = img.size

        cut_height = (h1-c_h)/2
        y1 = h1 -cut_height

        cropImg = img.crop((0,cut_height,w1,y1))
        cropImg.save(dir_name+'small/'+img_item,'JPEG',quality = 100)
    else:

        print(8888)
        true_width = (c_h / h) * w

        im.thumbnail((true_width, true_width), Image.ANTIALIAS)
        im.save(dir_name + 'small/' + img_item, 'JPEG', quality=100)

        img = Image.open(dir_name + 'small/' + img_item)
        w1, h1 = img.size

        cut_width = (w1 - c_w) / 2
        x1 = w1 - cut_width
        cropImg = im.crop((cut_width, 0,x1 , h1))
        cropImg.save(dir_name+'/small/'+img_item,'JPEG',quality = 100)


for item in dir_:
    try:
        if item=='small':
            continue
        print(item)
        cut_img(item)
    except (Exception) as e:
        print(e)
        pass

