# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from universities.models import University

from django.utils.translation import ugettext_lazy as _

    
class Club(models.Model):
    """
    Club with its details
    """
    title = models.CharField(_(u'Назва'), max_length=200)
    #university = models.ForeignKey(University)
    #while use just plain text university field
    university = models.CharField(max_length=1024, blank=True, null=False, default='')
    description = models.TextField(blank=True, null=False, default='')
    date = models.DateField(_(u'Дата створення'), default=datetime.now)
    address = models.TextField(_(u'Адреса'), blank=True)
    admin = models.ForeignKey(User)
    
    members = models.ManyToManyField(User, related_name='%(class)s_members', verbose_name=u"члени", blank=True)
    location = models.CharField(_(u'Місцезнаходження'), max_length=200)
	
    def __unicode__(self):
        return self.title

class Verification(models.Model):
	club = models.ForeignKey(Club)
	member = models.ForeignKey(User)
	is_approved = models.BooleanField(u'Підтвердити', default = True)

