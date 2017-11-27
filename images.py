from PIL import Image

catIm = Image.open(r'test/2b464aca5d3411e7894dac2b6ec319f9.png')

print(catIm.size)
quarter = catIm.resize((924,924))
quarter.save(r'test/quarter.png')
