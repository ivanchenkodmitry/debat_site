from django import template
import Image
import os

register = template.Library()


def resize_img(img, arg):
    #observe size from arg
    args = arg.split(',')
    width = args[0].strip()
    height = args[1].strip()
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        raise Exception(u'Wrong parameters for image size')
    base, ext = os.path.splitext(img.path)
    resized_path = ''.join([base, "_%i_%i" % (width, height), ext])
    if not os.path.exists(resized_path):
        original = Image.open(img.path)
        original.thumbnail((width, height), Image.ANTIALIAS)
        original.save(resized_path)
    base, ext = os.path.splitext(img.url)
    resized_url = ''.join([base, "_%i_%i" % (width, height), ext])
    return resized_url

    

register.filter('resize_img', resize_img)
