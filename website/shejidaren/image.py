import os
from PIL import Image
from helpers import file_dir

images = os.listdir(file_dir.get_upload_dir())

for item in images:
    if item.find('.') < 0:
        im = Image.open(file_dir.get_upload_dir()+item)
        im.save(file_dir.get_upload_dir()+item+".jpg")
        os.remove(file_dir.get_upload_dir() + item)

