import os
import ctypes
from random import randint

wall_dir = 'E:/Wallpaper'
images = os.listdir(wall_dir)
index = randint(0, len(images)-1)
image = wall_dir + '/' + images[index]
setImageAsBackground = ctypes.windll.user32.SystemParametersInfoW(20, 0,
                                                                  image, 0)
