# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from photos.models import UserGallery, UserPhoto

class UserGalleryForm(forms.ModelForm):
  class Meta:
        model = UserGallery
  def __init__(self, user=None, *args, **kwargs):
        self.user = user
       

class UserPhotoForm(forms.ModelForm):
    
    class Meta:
        model = UserPhoto
        
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserPhotoForm, self).__init__(*args, **kwargs)

class PhotoEditForm(forms.ModelForm):
    
    class Meta:
        model = UserPhoto
       
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(PhotoEditForm, self).__init__(*args, **kwargs)
