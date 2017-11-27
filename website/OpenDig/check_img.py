import os

img_dir = [
    r'201707/20170628/small_232/',
    r'201707/20170629/small_232/',
    r'201707/20170728/small_232/',
    r'201707/20170729/small_232/',
]

for dir_item in img_dir:
    print(dir_item)
    print('====================')
    img = os.listdir(dir_item)
    for item in img:
        print(dir_item+"t_232_140_"+item)
        os.rename(dir_item+item, dir_item+"t_232_140_"+item)

