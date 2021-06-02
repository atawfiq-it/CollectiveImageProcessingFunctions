from PIL import Image


class Variables():
    #Creating a one-pixel image for initializing the currImage
    mode = 'RGB'
    size = (1, 1)
    color = (0, 0, 0)
    currImage = Image.new(mode, size, color)