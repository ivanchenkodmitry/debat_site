# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _


from django.utils import simplejson
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode


from clubs.models import Club

class EventAddressWidget(Textarea):
    def render(self, name, value, attrs=None):
        result = super(EventAddressWidget, self).render(name, value, attrs=attrs)
        result += mark_safe(u'<input style ="float: right; margin-right: 33px; margin-top: 5px;"  type="button" value="Знайти на мапі" onclick="codeAddress()">')
        return result

class ClubForm(forms.ModelForm):
    location = forms.CharField(initial="(48.464954, 35.044956)", #dnipropetrovsk
                               widget=forms.HiddenInput)
    address = forms.CharField(label = _(u'Адреса'),widget=EventAddressWidget())
                               
    class Meta:
        model = Club
        exclude = ('members')
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ClubForm, self).__init__(*args, **kwargs)
    
