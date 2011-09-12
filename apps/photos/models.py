# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from photologue.models import Gallery, Photo

class UserGallery(models.Model):
    user = models.ForeignKey(User)
    gallery = models.OneToOneField(Gallery)

    def __unicode__(self):
        return self.title

class UserPhoto(Photo):
    user = models.ForeignKey(User)
    gallery = models.OneToOneField(Photo)

    def __unicode__(self):
        return self.title

