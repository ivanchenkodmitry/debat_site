# -*- coding: utf-8 -*- 

'''

Simple application for photos storeing

'''
from django.db import models
from PIL import Image
from django.db.models.signals import post_save, pre_delete
from django.conf import settings

import os

def get_thumbnail_path(image_path, size=150):
    thumbs_dir = 'thumbs_' + str(size)
    dirname, filename = os.path.split(image_path)
    dirname = os.path.join(dirname, thumbs_dir)
    if not os.path.exists(dirname):
        os.mkdir(dirname, 0755)
    return os.path.join(dirname, filename)

def create_thumbnail(image_path, size=150):
    thumb_path = get_thumbnail_path(image_path, size)
    delete_thumbnail(image_path, size)
    img = Image.open(image_path)
    img.thumbnail((size, size), Image.ANTIALIAS)
    img.save(thumb_path)

def delete_thumbnail(image_path, size=150):
    thumb_path = get_thumbnail_path(image_path, size)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)

def get_thumbnail_url(image_url, size=150):
    thumbs_part = 'thumbs_' + str(size)
    image_url_parts = image_url.rsplit('/', 1)
    return image_url_parts[0] + '/' + thumbs_part + '/' + image_url_parts[1]

class Photo(models.Model):
    
    image = models.ImageField(upload_to = "image/uploads")
    title = models.CharField(max_length = 256, null=True, blank=True)
    
 
    def get_thumbnail_html(self):
        html = '<a class="image-picker" href="%s"><img src="%s" alt="%s"/></a>' % (self.image.url, get_thumbnail_url(self.image.url), self.title)
        return html
    get_thumbnail_html.short_description = u'Иконка'
    get_thumbnail_html.allow_tags = True

def post_save_handler(sender, **kwargs):
    create_thumbnail(kwargs['instance'].image.path)
post_save.connect(post_save_handler, sender=Photo)

def pre_delete_handler(sender, **kwargs):
    delete_thumbnail(kwargs['instance'].image.path)
pre_delete.connect(pre_delete_handler, sender=Photo)


