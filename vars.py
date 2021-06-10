from PIL import Image


class Variables():
    #Creating a one-pixel image for initializing the currImage
    mode = 'RGB'
    size = (100, 100)
    color = (255, 255, 255)
    image_size = 320
    currImage = Image.new(mode, size, color)
    modifiedImage = Image.new(mode, size, color)