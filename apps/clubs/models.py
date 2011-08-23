# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from universities.models import University

from django.utils.translation import ugettext_lazy as _

class Members(models.Model):
	user = models.ForeignKey(User)
	approved = models.BooleanField(u'Підтвердити', default = False)
    
	def __unicode__(self):
		return self.user.get_profile().surname + ' ' + self.user.get_profile().name
        class Meta:
            verbose_name = _('Члени')
            verbose_name_plural = _('Члени')
    
class Club(models.Model):
    """
    Club with its details
    """
    title = models.CharField(_(u'Назва'), max_length=200)
    university = models.ForeignKey(University)
    date = models.DateField(_(u'Дата створення'), default=datetime.now)
    address = models.TextField(_(u'Адреса'), blank=True)
    admin = models.ForeignKey(User)
    
    members = models.ManyToManyField(Members, related_name='%(class)s_members', verbose_name=u"члени", blank=True)
    location = models.CharField(_(u'Місцезнаходження'), max_length=200)
	
    def __unicode__(self):
        return self.title


	
