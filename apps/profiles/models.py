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
        ('Методична робота', _('Методична робота')),
        ('Розвиток англійських дебатів', _('Розвиток англійських дебатів')),
        ('Організація дебатних заходів', _('Організація дебатних заходів')),
        ('Співпраця із комерційними структурами', _('Співпраця із комерційними структурами')),
        ('Співпраця  із іншими ГО', _('Співпраця  із іншими ГО')),
        ('Співпраця із ЗМІ', _('Співпраця із ЗМІ')),
        ('Не хочу займатись організаційними справами', _('Не хочу займатись організаційними справами')),
    )

    MEMBERS_FEE = (
        ('5 грн', _('5 грн')),
        ('10 грн', _('10 грн')),
        ('15 грн', _('15 грн')),
        ('20 грн', _('20 грн')),
        ('30 грн', _('30 грн')),
        ('50 грн', _('50 грн')),
        ('Не можу сплачувати членський внесок', _('Не можу сплачувати членський внесок')),
    )
    
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))

    surname =  models.CharField(_('Прізвище'), max_length=200)
    name = models.CharField(_('Ім’я'), max_length=200)
    middle_name = models.CharField(_('По батькові'), max_length=200)
    birth_date = models.CharField(_('Дата народження'), max_length=300)
    address = models.TextField(_('Поштова адреса'), null=True, max_length=200)
    phone = models.CharField(_('Мобільний телефон'), null=True, max_length=200)
    skype = models.CharField(_('Логін Skype'), null=True, blank=True, max_length=200)
    icq = models.CharField(_('ICQ'), null=True, blank=True, max_length=200,)
    website = models.URLField(_('Адреса сторінки в соціальній мережі'), null=True, blank=True, verify_exists=False)
    education = models.CharField(_('Освіта (ВНЗ, факультет)'), blank=True, max_length=500)
    work = models.CharField(_('Місце роботи'), null=True, blank=True, max_length=600)
    experience = models.CharField(_('Досвід гри у дебати'), null=True, blank=True, max_length=600)
    club = models.ForeignKey(Club, null=True, blank=True, unique=False, verbose_name=_('club'))
    social_work_exp = models.CharField(_('Досвід громадської роботи'), null=True, blank=True, max_length=600)
    desired_exp = models.TextField(_('Досвід, який хочу отримати'), null=True, blank=True)

    org_way = models.CharField(_('Організаційний напрямок'), null=True, choices = ORG_WAYS, max_length=200)
    members_fee = models.CharField(_('Членські внески'), choices = MEMBERS_FEE, max_length=200)  
    interests = models.TextField(_('Інтереси'), null=True, blank=True)
    vk_id = models.CharField(_('ID Вконтакті'), null=True, blank=True, max_length=30)
    about = models.TextField(_('about'), null=True, blank=True)

    
    def __unicode__(self):
        return self.name + ' ' + self.surname
    
    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)
    
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)

class Verification(models.Model):
	md5_hash = models.CharField(_('Md5 for verivication'), null=True, blank=True, max_length=100)
	profile = models.OneToOneField(Profile, null=True, blank=True, verbose_name=_('profile'))



