#!/usr/bin/env python

from PIL import Image
import os,string,math
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# dir_name = r'201706/27/1/'
dir_name = r'test/'
thumb_dir = r'small/'

dir_ = os.listdir(dir_name)

def cut_img(img_item):

    c_w=232
    c_h=140

    if not os.path.exists(dir_name+'small'):
        os.makedirs(dir_name+'small')

    # if os.path.exists(dir_name+thumb_dir+img_item):
    #     return True

    im = Image.open(dir_name+img_item)
    im = im.convert('RGB')

    w,h = im.size

    if( w > h ):
        # 这种情况都是减少 w 为主
        if (w/h) < (c_w/c_h):
            print(1)
            resize_height = math.ceil(c_w/w*h)
            quarter = im.resize((c_w, resize_height))
            quarter.save(dir_name + thumb_dir + img_item)

            img = Image.open(dir_name + thumb_dir + img_item)
            w1, h1 = img.size
            cut_height = (h1 - c_h) / 2
            y1 = h1 - cut_height
            cropImg = img.crop((0, cut_height, w1, y1))
            cropImg.save(dir_name + thumb_dir + img_item, 'JPEG', quality=100)
        else:
            print(2)
            resize_width = math.ceil(c_h/h*w)
            quarter = im.resize((resize_width, c_h))
            quarter.save(dir_name + thumb_dir + img_item, 'JPEG', quality=100)

            img = Image.open(dir_name + thumb_dir + img_item)
            w1, h1 = img.size
            cut_width = (w1 - c_w) / 2
            x1 = w1 - cut_width
            cropImg = img.crop((cut_width, 0, x1, h1))
            cropImg.save(dir_name + '/small/' + img_item, 'JPEG', quality=100)
    else:
        if (w/h) < (c_w/c_h):
            print(3)
            resize_height = math.ceil(c_w/w*h)
            quarter = im.resize((c_w, resize_height))
            quarter.save(dir_name + thumb_dir + img_item, 'JPEG', quality=100)
            # temp_w,temp_h = im.size
            # if temp_w != c_w:
            #     after_height = round(c_w / w * h)
            #     im.thumbnail((after_height, after_height), Image.ANTIALIAS)
            #     im.save(dir_name + thumb_dir + img_item, 'JPEG', quality=100)

            img = Image.open(dir_name + thumb_dir + img_item)
            w1, h1 = img.size
            cut_height = (h1 - c_h) / 2
            y1 = h1 - cut_height
            cropImg = img.crop((0, cut_height, w1, y1))
            cropImg.save(dir_name + thumb_dir + img_item, 'JPEG', quality=100)
        else:
            print(4)
            resize_width = math.ceil(c_h/h*w)
            quarter = im.resize((resize_width, c_h))
            quarter.save(dir_name + thumb_dir + img_item, 'JPEG', quality=100)

            img = Image.open(dir_name + thumb_dir + img_item)
            w1, h1 = img.size
            cut_height = (h1 - c_h) / 2
            y1 = h1 - cut_height
            cropImg = img.crop((0, cut_height, w1, y1))
            cropImg.save(dir_name + thumb_dir + img_item, 'JPEG', quality=100)

for item in dir_:
    try:
        if item==thumb_dir[:-1]:
            exit()
        print(item)
        cut_img(item)
        print('-----------------')
    except (Exception) as e:
        print(e)
        pass

