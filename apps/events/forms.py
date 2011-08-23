# -*- coding: utf-8 -*-
from django import forms
from events.models import Event, Member


class EventForm(forms.ModelForm):
    questions = forms.CharField(widget=forms.widgets.HiddenInput())
    location = forms.CharField(initial="(48.464954, 35.044956)", #dnipropetrovsk
                               widget=forms.widgets.HiddenInput())
    
    class Meta:
        model = Event
        exclude = ('members', 'creator')
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user        
        super(EventForm, self).__init__(*args, **kwargs)

