# -*- coding: utf-8 -*-
from django.db import models

from django.utils.translation import ugettext_lazy as _

		
class University(models.Model):
    title = models.CharField(_(u'Назва'), max_length=200, primary_key=True)
    address = models.TextField(_(u'Адреса'))
    site = models.CharField(_(u'Сайт'), max_length=200)
       
       
    class Meta:
        ordering = ['title']
        verbose_name = _('university')
        verbose_name_plural = _('universities')

   
    def __unicode__(self):
         return self.title

