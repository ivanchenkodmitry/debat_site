# -*- coding: utf-8 -*-
from imagekit.specs import ImageSpec 
from imagekit import processors 
from imagekit.lib import *

# first we define our thumbnail resize processor 
class ResizeThumb(processors.Resize): 
    width = 100 
    height = 75 
    crop = True

# now lets create an adjustment processor to enhance the image at small sizes 
class EnchanceThumb(processors.Adjustment): 
    contrast = 1.2 
    sharpness = 1.1 

# now we can define our thumbnail spec 
class Thumbnail(ImageSpec): 
    processors = [ResizeThumb, EnchanceThumb]
