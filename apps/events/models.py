from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic

#from photologue.models import *

#from tagging.fields import TagField

from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson

class Member(models.Model):
	user = models.ForeignKey(User)
	answers = models.TextField(blank=True)
    
	def __unicode__(self):
		return self.user.get_profile().surname + ' ' + self.user.get_profile().name

class Event(models.Model):
    """
    An event with its details
    """
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    date = models.DateTimeField(_('date'), default=datetime.now)
    address = models.TextField(_('addres'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    creator = models.ForeignKey(User)
    members = models.ManyToManyField(Member, verbose_name="members_list", blank=True)
    location = models.CharField(_('location'), max_length=200)
    questions = models.TextField(blank=True)
    approved = models.BooleanField(_('approved'), default = False)
    
    def __unicode__(self):
        return self.title
        
    def get_table_data(self):
        """
        Get answer table data
        """
        data = {}
                
        if self.questions != "":
        
            questions = simplejson.loads(self.questions)
            
            data['columns'] = [_("Member")]
            
            for question in questions:
                data['columns'].append(question['title'])
            
            members = self.members.exclude(answers="")
            
            data['rows'] = []
            
            for member in members:
                answers = simplejson.loads(member.answers)
                row = []
                row.append({"data": unicode(member),"profile": member.user.username, "type":"profile"})
                for i, answer in enumerate(answers):
                    if questions[i]['type'] == "one":
                        row.append({"data": questions[i]['options'][int(answer)-1]})
                    elif questions[i]['type'] == "multi":
                        items = []
                        for j in answer:
                            items.append(questions[i]['options'][int(j)-1])
                        row.append({"data": items, "type":"list"})
                    else:
                        row.append({"data": answer})
                data['rows'].append(row)
        
        return data
        
    def get_excel_data(self):
        """
        Get data for ExcelResponse
        """
        data = []
                
        if self.questions != "":
        
            questions = simplejson.loads(self.questions)
            
            headers = [unicode(_("Member"))]
            
            for question in questions:
                headers.append(question['title'])
                
            data.append(headers)
            
            members = self.members.exclude(answers="")
            
            for member in members:
                answers = simplejson.loads(member.answers)
                row = []
                row.append(unicode(member))
                for i, answer in enumerate(answers):
                    if questions[i]['type'] == "one":
                        row.append(questions[i]['options'][int(answer)-1])
                    elif questions[i]['type'] == "multi":
                        value = u""
                        for j in answer:
                            value = value + u"- %s\n" % questions[i]['options'][int(j)-1]
                        row.append(value)
                    else:
                        row.append(answer)
                data.append(row)
        
        return data
