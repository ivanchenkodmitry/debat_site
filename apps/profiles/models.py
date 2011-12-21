# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from timezones.fields import TimeZoneField
from clubs.models import Club


class Profile(models.Model):
    
    ORG_WAYS = (
        (u'Методична робота', _(u'Методична робота')),
        (u'Розвиток англійських дебатів', _(u'Розвиток англійських дебатів')),
        (u'Організація дебатних заходів', _(u'Організація дебатних заходів')),
        (u'Співпраця із комерційними структурами', _(u'Співпраця із комерційними структурами')),
        (u'Співпраця  із іншими ГО', _(u'Співпраця  із іншими ГО')),
        (u'Співпраця із ЗМІ', _(u'Співпраця із ЗМІ')),
        (u'Не хочу займатись організаційними справами', _(u'Не хочу займатись організаційними справами')),
    )

    MEMBERS_FEE = (
        (u'5 грн', _(u'5 грн')),
        (u'10 грн', _(u'10 грн')),
        (u'15 грн', _(u'15 грн')),
        (u'20 грн', _(u'20 грн')),
        (u'30 грн', _(u'30 грн')),
        (u'50 грн', _(u'50 грн')),
        (u'Не можу сплачувати членський внесок', _(u'Не можу сплачувати членський внесок')),
    )
    
    user = models.ForeignKey(User, unique=True, verbose_name=_(u'user'))

    surname =  models.CharField(_(u'Прізвище'), max_length=200)
    name = models.CharField(_(u'Ім’я'), max_length=200)
    middle_name = models.CharField(_(u'По батькові'), max_length=200)
    birth_date = models.CharField(_(u'Дата народження'), max_length=300)
    address = models.TextField(_(u'Поштова адреса'), null=True, max_length=200)
    phone = models.CharField(_(u'Мобільний телефон'), null=True, max_length=200)
    skype = models.CharField(_(u'Логін Skype'), null=True, blank=True, max_length=200)
    icq = models.CharField(_(u'ICQ'), null=True, blank=True, max_length=200,)
    website = models.URLField(_(u'Адреса сторінки в соціальній мережі'), null=True, blank=True, verify_exists=False)
    education = models.CharField(_(u'Освіта (ВНЗ, факультет)'), blank=True, max_length=500)
    work = models.CharField(_(u'Місце роботи'), null=True, blank=True, max_length=600)
    experience = models.CharField(_(u'Досвід гри у дебати'), null=True, blank=True, max_length=600)
#    club = models.ForeignKey(Club, null=True, blank=True, unique=False, verbose_name=_(u'club'))
    social_work_exp = models.CharField(_(u'Досвід громадської роботи'), null=True, blank=True, max_length=600)
    desired_exp = models.TextField(_(u'Досвід, який хочу отримати'), null=True, blank=True)

    org_way = models.CharField(_(u'Організаційний напрямок'), null=True, choices = ORG_WAYS, max_length=200)
    members_fee = models.CharField(_(u'Членські внески'), choices = MEMBERS_FEE, max_length=200)  
    interests = models.TextField(_(u'Інтереси'), null=True, blank=True)
    vk_id = models.CharField(_(u'ID Вконтакті'), null=True, blank=True, max_length=30)
    about = models.TextField(_(u'about'), null=True, blank=True)

    
    def __unicode__(self):
        return self.name + ' ' + self.surname
    
    def __repr__(self):
        return self.name + ' ' + self.surname
    
    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)
    
    class Meta:
        verbose_name = _(u'profile')
        verbose_name_plural = _(u'profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)

class Verification(models.Model):
    md5_hash = models.CharField(_(u'Md5 for verivication'), null=True, blank=True, max_length=100)
    profile = models.OneToOneField(Profile, null=True, blank=True, verbose_name=_(u'profile'))



