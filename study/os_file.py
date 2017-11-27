import shutil,os,send2trash,zipfile

exampleZip = zipfile.ZipFile('img4.zip')
result = exampleZip.namelist()
print(result)

img4Info = exampleZip.getinfo('img4/5913bc52235c8jk5q8XvFFnJxA6vD.jpg')
print(img4Info.file_size)