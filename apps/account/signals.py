# -*- coding: utf-8 -*-
from emailconfirmation.signals import email_confirmed
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

def mail_to_admin(sender, email_address, **kwargs):
	email_address.user.is_active = False
	email_address.user.save()

	html = get_template('mail_profile.html')
	try:
		domain = Site.objects.all()[0].domain
	except:
		domain = 'example.com'
	mail_context = Context({ 'user': email_address.user, 'domain':domain })
	admins = User.objects.filter(is_superuser = True)
	emails = []
	for admin in admins:
		emails = emails + [admin.email]
	EMAIL_RECIPIENTS = emails
	subject, from_email, to = 'Новий користувач на сайті Дебатної організації', settings.SERVER_EMAIL, EMAIL_RECIPIENTS
	html_content = html.render(mail_context)
	msg = EmailMultiAlternatives(subject, u'Новий користувач на сайті Дебатної організації', from_email, to)
	msg.attach_alternative(html_content, "text/html")
	msg.send()

email_confirmed.connect(mail_to_admin)
