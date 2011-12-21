# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic
from photos.models import PhotoSet
#from photologue.models import *
from stdimage import StdImageField
#from tagging.fields import TagField

from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson

TITLE_EXCERPT_LENGTH = 22

class Event(models.Model):
    """
    An event with its details
    """
    title = models.CharField(_(u'Назва'), max_length=50)
    description = models.TextField(_(u'Опис'), blank=True)
    date_begin = models.DateTimeField(_(u'Початок'), default=datetime.now)
    date_end = models.DateTimeField(_(u'Кінець'), default=datetime.now)
    address = models.TextField(_(u'Адреса проведення'), blank=True)
    date_added = models.DateTimeField(_(u'Дата створення'), default=datetime.now, editable=False)
    creator = models.ForeignKey(User, related_name="%(class)s_created")
    members = models.ManyToManyField(User, related_name='events', verbose_name=_(u'Учасники'))
    location = models.CharField(_(u'location'), max_length=200)
    questions = models.TextField(blank=True)
    approved = models.BooleanField(_(u'Підтверджено'), default = False)
    eventimage = StdImageField(_(u'Лого події'),upload_to = "photos/", size=(400, 300), thumbnail_size=(100, 100))
    gallery = models.ForeignKey(PhotoSet, blank = True, null = True)
    def __unicode__(self):
        return self.title
        
    def user_is_member(self, user):
        return user in self.members.all()
        
    @property
    def title_excerpt(self):
        if len(self.title) > TITLE_EXCERPT_LENGTH:
            result = ''.join([self.title[:TITLE_EXCERPT_LENGTH], '...'])
        else:
            result = self.title
        return result
        
    def get_table_data(self):
        """
        Get answer table data
        """
        data = {}
                
        if self.questions != "":
        
            questions = simplejson.loads(self.questions)
            
            data['columns'] = [_(u"Учасник")]
            
            for question in questions:
                data['columns'].append(question['title'])
                
            answer_lists = AnswerList.objects.filter(event=self)
            
            data['rows'] = []
            
            for answer_list in answer_lists:
                answers = simplejson.loads(answer_list.value)
                row = []
                row.append({"data": unicode(answer_list.user.get_profile()),
                            "profile": answer_list.user.username, "type":"profile"})
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
            
            headers = [unicode(_(u"Учасник"))]
            
            for question in questions:
                headers.append(question['title'])
                
            data.append(headers)
            
            answer_lists = AnswerList.objects.filter(event=self)
            
            for answer_list in answer_lists:
                answers = simplejson.loads(answer_list.value)
                row = []
                row.append(unicode(answer_list.user.get_profile()))
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
class AnswerList(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    value = models.TextField()

