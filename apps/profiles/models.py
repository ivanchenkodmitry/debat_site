# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from timezones.fields import TimeZoneField

class Profile(models.Model):
    
    ORG_WAYS = (
        (1, _('')),
        (2, _('Методична робота')),
        (3, _('Розвиток англійських дебатів')),
        (4, _('Організація дебатних заходів')),
        (5, _('Співпраця із комерційними структурами')),
        (6, _('Співпраця  із іншими ГО')),
        (7, _('Співпраця із ЗМІ')),
        (8, _('Не хочу займатись організаційними справами')),
    )

    MEMBERS_FEE = (
        (1, _('5 грн')),
        (2, _('10 грн')),
        (3, _('15 грн')),
        (4, _('20 грн')),
        (5, _('30 грн')),
        (6, _('50 грн')),
        (7, _('Не можу сплачувати членський внесок')),
    )
    
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))

    surname =  models.CharField(_('Прізвище'), max_length=30)
    name = models.CharField(_('Ім’я'), max_length=50, blank=True)
    middle_name = models.CharField(_('По батькові'), max_length=30)
    birth_date = models.CharField(_('Дата народження'), max_length=30)
    mail = models.CharField(_('Поштова адреса'), null=True, max_length=30)
    phone = models.CharField(_('Мобільний телефон'), null=True, max_length=30)
    skype = models.CharField(_('Логін Skype'), null=True, max_length=30)
    icq = models.CharField(_('ICQ'), null=True, max_length=30,)
    website = models.URLField(_('Адреса сторінки в соціальній мережі'), null=True, blank=True, verify_exists=False)
    education = models.CharField(_('Освіта (ВНЗ, факультет)'), max_length=30)
    work = models.CharField(_('Місце роботи'), max_length=30)
    experience = models.CharField(_('Досвід гри у дебати'), max_length=30)
    club = models.CharField(_('Дебатний клуб'), max_length=30)
    social_work_exp = models.CharField(_('Досвід громадської роботи'), max_length=30)
    desired_exp = models.TextField(_('Досвід, який хочу отримати'), null=True, blank=True)
    org_way = models.TextField(_('Організаційний напрямок'), null=True, choices = ORG_WAYS)
    members_fee = models.IntegerField(_('Членські внески'), null=True, choices = MEMBERS_FEE)  
    interests = models.TextField(_('Інтереси'), null=True, blank=True)
    vk_id = models.TextField(_('ID Вконтакті'), null=True, blank=True)

    admin_verificatin = models.BooleanField(_("admin_verivication"))   #Проверка пользователья Админом
    about = models.TextField(_('about'), null=True, blank=True)

    
    def __unicode__(self):
        return self.user.username
    
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
