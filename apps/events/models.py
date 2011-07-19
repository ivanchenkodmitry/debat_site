from django.db import models
from django.contrib.auth.models import User
#from datetime import datetime
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic

#from photologue.models import *

#from tagging.fields import TagField

from django.utils.translation import ugettext_lazy as _

class Member(models.Model):
	user = models.ForeignKey(User)
    
	def __unicode__(self):
		return self.user.username


class Event(models.Model):
    """
    An event with its details
    """
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    date = models.CharField(_('date added'), max_length=200)
    address = models.TextField(_('addres'), blank=True)
    date_added = models.CharField(_('date added'), max_length=200)
    creator = models.ForeignKey(User)
    members = models.ManyToManyField(Member, verbose_name="members_list", blank=True)
	
    def __unicode__(self):
        return self.title


	
