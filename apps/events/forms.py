# -*- coding: utf-8 -*-
from django import forms
from events.models import Event, Member


class EventForm(forms.ModelForm):
  
  class Meta:
        model = Event
        exclude = ('location', 'members', 'creator')
        
  def __init__(self, user=None, *args, **kwargs):
        self.user = user        
        super(EventForm, self).__init__(*args, **kwargs)
        
  def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)
        event.creator = self.user
        if commit:
            event.save()
            member = Member(user = self.user)
            member.save()
            event.members.add(member)
            event.save()
        return event
