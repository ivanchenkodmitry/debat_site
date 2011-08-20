# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from clubs.models import Club


class ClubForm(forms.ModelForm):
    location = forms.CharField(initial="(48.464954, 35.044956)", #dnipropetrovsk
                               widget=forms.HiddenInput)
                               
    class Meta:
        model = Club
        exclude = ('members')
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ClubForm, self).__init__(*args, **kwargs)
    
