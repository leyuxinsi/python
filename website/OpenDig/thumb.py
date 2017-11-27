import os
from PIL import Image

img_dir = r'201706/27/1/big/'
img = os.listdir(img_dir)

for item in img:
    try:
        im = Image.open(img_dir + item)
        w, h = im.size
        print(w, h)
        if w > 500 and h > 500:
            im.thumbnail((500, 500), Image.ANTIALIAS)
            im.save(img_dir + item)
            print(item)
    except:
        print(item)
