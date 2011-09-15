# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from tagging.fields import TagField
from tagging.models import Tag
from photologue.models import *
from pytils.translit import slugify

class Project(models.Model):
    """Post model."""

    title           = models.CharField(u'Назва', max_length=200)
    author          = models.ForeignKey(User, related_name="added_projects")
    creator_ip      = models.IPAddressField(_(u"IP адреса автора повідомлення"), blank=True, null=True)
    body            = models.TextField(_(u'Повідомлення'))
   
    created_at      = models.DateTimeField(_(u'Створено'), default=datetime.now)
    
    
    
    class Meta:
        verbose_name        = _('project')
        ordering            = ('-created_at',)
        

    def __unicode__(self):
        return self.title

''' def get_absolute_url(self):
        return ('project', None, {
            'username': self.author.username,
            'year': self.publish.year,
            'month': "%02d" % self.publish.month,
            'slug': self.slug
    })
    get_absolute_url = models.permalink(get_absolute_url)

    


 handle notification of new comments
from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Project):
        project = instance.content_object
        
models.signals.project_save.connect(new_comment, sender=ThreadedComment)'''
