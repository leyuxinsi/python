from PIL import Image,ImageDraw

# 打开一个jpg图像文件，注意路径要改成你自己的:
im_bg = Image.open('image/small_background.png')

im_up = Image.open('image/small_4b4eec265ed711e7b69df079595db843.png')
print(im_bg.size)
im_obj = Image.blend(im_bg,im_up,0.8)
im_obj.save('image/ccc.png')

