# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from universities.models import University


class UniversityForm(forms.ModelForm):
  
  class Meta:
        model = University
        
        
  def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UniversityForm, self).__init__(*args, **kwargs)
    