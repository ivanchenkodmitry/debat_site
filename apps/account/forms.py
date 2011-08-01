# -*- coding: utf-8 -*-
import re

from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import smart_unicode
from django.utils.hashcompat import sha_constructor

from pinax.core.utils import get_send_mail
send_mail = get_send_mail()

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from emailconfirmation.models import EmailAddress
from account.models import Account

from timezones.forms import TimeZoneField

from account.models import PasswordReset

from recaptcha.fields import ReCaptchaField


alnum_re = re.compile(r'^\w+$')

class LoginForm(forms.Form):
    
    username = forms.CharField(label=_("Username"), max_length=30, widget=forms.TextInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False))
    remember = forms.BooleanField(label=_("Remember Me"), help_text=_("If checked you will stay logged in for 3 weeks"), required=False)
    
    user = None
    
    def clean(self):
        if self._errors:
            return
        user = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"])
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is currently inactive."))
        else:
            raise forms.ValidationError(_("The username and/or password you specified are not correct."))
        return self.cleaned_data
    
    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            request.user.message_set.create(message=ugettext(u"Successfully logged in as %(username)s.") % {'username': self.user.username})
            if self.cleaned_data['remember']:
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return True
        return False


class SignupForm(forms.Form):

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
    
    username = forms.CharField(label=_(u'Логін'),  max_length=30, widget=forms.TextInput())
    surname =  forms.CharField(label=_(u'Прізвище'), max_length=30, widget=forms.TextInput())
    name =  forms.CharField(label=_(u'Ім’я'), max_length=30, widget=forms.TextInput())
    middle_name = forms.CharField(label=_(u'По батькові'), max_length=30, widget=forms.TextInput())
    birth_date = forms.DateField(label=_(u'Дата народження'))
    mail = forms.CharField(label=_(u'Поштова адреса'), required = False, max_length=30, widget=forms.TextInput())
    phone = forms.CharField(label=_(u'Мобільний телефон'), required = False, max_length=30, widget=forms.TextInput())
    skype = forms.CharField(label=_(u'Логін Skype'), required = False, max_length=30, widget=forms.TextInput())
    icq = forms.IntegerField(label=_(u'ICQ'), max_value=999999999, required = False, widget=forms.TextInput())
    website = forms.URLField(label=_(u'Адреса сторінки в соціальній мережі (вконтакті, facebook тощо)'), required = False)
    education = forms.CharField(label=_(u'Освіта (ВНЗ, факультет)'), required = False, max_length=30, widget=forms.TextInput())
    work = forms.CharField(label=_(u'Місце роботи'), required = False, max_length=150, widget=forms.TextInput())
    experience = forms.CharField(label=_(u'Опишіть у довільній формі досвід гри у дебати (роки участі у дебатах, турніри, в яких Ви брали участь, тощо).'), required = False, max_length=30, widget=forms.TextInput())
    club = forms.CharField(label=_(u'Дебатний клуб, який  представляєте (якщо є)'), required = False, max_length=30, widget=forms.TextInput())
    social_work_exp = forms.CharField(label=_(u'Який досвід громадської роботи ви маєте(реалізовані проекти, членство в ГО, студ.самоврядуванні і т.д.)?'), required = False, max_length=30, widget=forms.TextInput())
    desired_exp = forms.CharField(label=_(u'Які знання, досвід чи вміння ви хочете отримати, ставши членом ВМГО «ФДУ»?'),  required = False, max_length=30, widget=forms.TextInput())

    org_way = forms.ChoiceField(label=_(u'Яким організаційним напрямком в діяльності ВМГО «ФДУ» ви хотіли б займатись?'), choices = ORG_WAYS, initial='1', required = False, widget=forms.Select())

    members_fee = forms.ChoiceField(label=_(u'Який членський внесок ви готові сплачувати щомісячно?'), choices = MEMBERS_FEE, initial='1', required = False, widget=forms.Select())

    interests = forms.CharField(label=_(u'Напишіть, будь ласка, про свої цікаві захоплення та вміння'), required = False, max_length=30, widget=forms.TextInput())

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput(render_value=False))
    vk_id = forms.CharField(label = _('ID Вконтакті')) #, widget= forms.HiddenInput())

    
    if settings.ACCOUNT_REQUIRED_EMAIL or settings.ACCOUNT_EMAIL_VERIFICATION:
        email = forms.EmailField(
            label = _("Email"),
            required = True,
            widget = forms.TextInput()
        )
    else:
        email = forms.EmailField(
            label = _("Email (optional)"),
            required = False,
            widget = forms.TextInput()
        )

    recaptcha = ReCaptchaField(error_messages = {  
            'required': u'Это поле должно быть заполнено',            
            'invalid' : u'Указанное значение было неверно'  
            })
    
    confirmation_key = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))
    
    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data
    
    def save(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]

       
        if self.cleaned_data["confirmation_key"]:
            from friends.models import JoinInvitation # @@@ temporary fix for issue 93
            try:
                join_invitation = JoinInvitation.objects.get(confirmation_key = self.cleaned_data["confirmation_key"])
                confirmed = True
            except JoinInvitation.DoesNotExist:
                confirmed = False
        else:
            confirmed = False
        
        # @@@ clean up some of the repetition below -- DRY!
        
        if confirmed:
            if email == join_invitation.contact.email:
                new_user = User.objects.create_user(username, email, password)
                join_invitation.accept(new_user) # should go before creation of EmailAddress below
                new_user.message_set.create(message=ugettext(u"Your email address has already been verified"))
                # already verified so can just create
                EmailAddress(user=new_user, email=email, verified=True, primary=True).save()
            else:
                new_user = User.objects.create_user(username, "", password)
                join_invitation.accept(new_user) # should go before creation of EmailAddress below
                if email:
                    new_user.message_set.create(message=ugettext(u"Confirmation email sent to %(email)s") % {'email': email})
                    EmailAddress.objects.add_email(new_user, email)
        else:
            new_user = User.objects.create_user(username, "", password)
            if email:
                new_user.message_set.create(message=ugettext(u"Confirmation email sent to %(email)s") % {'email': email})
                EmailAddress.objects.add_email(new_user, email)
                
        profile = new_user.get_profile()
        profile.surname = self.cleaned_data["surname"]
        profile.name =  self.cleaned_data["name"]
        profile.middle_name = self.cleaned_data["middle_name"]
        profile.birth_date = self.cleaned_data["birth_date"]
        profile.mail = self.cleaned_data["mail"]
        profile.phone = self.cleaned_data["phone"]
        profile.skype = self.cleaned_data["skype"]
        profile.icq = self.cleaned_data["icq"]
        profile.website = self.cleaned_data["website"]
        profile.education = self.cleaned_data["education"]
        profile.work = self.cleaned_data["work"]
        profile.experience = self.cleaned_data["experience"]
        profile.club = self.cleaned_data["surname"]
        profile.social_work_exp = self.cleaned_data["social_work_exp"]
        profile.desired_exp = self.cleaned_data["desired_exp"]
        profile.org_way = self.cleaned_data["org_way"]
        profile.members_fee = self.cleaned_data["members_fee"]
        profile.interests = self.cleaned_data["interests"]
        profile.vk_id = self.cleaned_data["vk_id"]

        profile.save()
        
        if settings.ACCOUNT_EMAIL_VERIFICATION:
            new_user.is_active = False
            new_user.save()
                
        return username, password # required for authenticate()


class OpenIDSignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput())
    
    if settings.ACCOUNT_REQUIRED_EMAIL or settings.ACCOUNT_EMAIL_VERIFICATION:
        email = forms.EmailField(
            label = _("Email"),
            required = True,
            widget = forms.TextInput()
        )
    else:
        email = forms.EmailField(
            label = _("Email (optional)"),
            required = False,
            widget = forms.TextInput()
        )
    
    def __init__(self, *args, **kwargs):
        # remember provided (validated!) OpenID to attach it to the new user
        # later.
        self.openid = kwargs.pop("openid", None)
        
        # pop these off since they are passed to this method but we can't
        # pass them to forms.Form.__init__
        kwargs.pop("reserved_usernames", [])
        kwargs.pop("no_duplicate_emails", False)
        
        super(OpenIDSignupForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(u"Usernames can only contain letters, numbers and underscores.")
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError(u"This username is already taken. Please choose another.")


class UserForm(forms.Form):
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class AccountForm(UserForm):
    
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        try:
            self.account = Account.objects.get(user=self.user)
        except Account.DoesNotExist:
            self.account = Account(user=self.user)


class AddEmailForm(UserForm):
    
    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput(attrs={'size':'30'}))
    
    def clean_email(self):
        try:
            EmailAddress.objects.get(user=self.user, email=self.cleaned_data["email"])
        except EmailAddress.DoesNotExist:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_("This email address already associated with this account."))
    
    def save(self):
        self.user.message_set.create(message=ugettext(u"Confirmation email sent to %(email)s") % {'email': self.cleaned_data["email"]})
        return EmailAddress.objects.add_email(self.user, self.cleaned_data["email"])


class ChangePasswordForm(UserForm):
    
    oldpassword = forms.CharField(label=_("Current Password"), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("New Password (again)"), widget=forms.PasswordInput(render_value=False))
    
    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["oldpassword"]
    
    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password2"]
    
    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        self.user.save()
        self.user.message_set.create(message=ugettext(u"Password successfully changed."))


class SetPasswordForm(UserForm):
    
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput(render_value=False))
    
    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password2"]
    
    def save(self):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()
        self.user.message_set.create(message=ugettext(u"Password successfully set."))


class ResetPasswordForm(forms.Form):
    
    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput(attrs={'size':'30'}))
    
    def clean_email(self):
        if EmailAddress.objects.filter(email__iexact=self.cleaned_data["email"], verified=True).count() == 0:
            raise forms.ValidationError(_("Email address not verified for any user account"))
        return self.cleaned_data["email"]
    
    def save(self):
        for user in User.objects.filter(email__iexact=self.cleaned_data["email"]):
            temp_key = sha_constructor("%s%s%s" % (
                settings.SECRET_KEY,
                user.email,
                settings.SECRET_KEY,
            )).hexdigest()
            
            # save it to the password reset model
            password_reset = PasswordReset(user=user, temp_key=temp_key)
            password_reset.save()
            
            current_site = Site.objects.get_current()
            domain = unicode(current_site.domain)
            
            #send the password reset email
            subject = _("Password reset email sent")
            message = render_to_string("account/password_reset_key_message.txt", {
                "user": user,
                "temp_key": temp_key,
                "domain": domain,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], priority="high")
        return self.cleaned_data["email"]


class ResetPasswordKeyForm(forms.Form):
    
    password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("New Password (again)"), widget=forms.PasswordInput(render_value=False))
    temp_key = forms.CharField(widget=forms.HiddenInput)
    
    def clean_temp_key(self):
        temp_key = self.cleaned_data.get("temp_key")
        if not PasswordReset.objects.filter(temp_key=temp_key, reset=False).count() == 1:
            raise forms.ValidationError(_("Temporary key is invalid."))
        return temp_key
    
    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password2"]
    
    def save(self):
        # get the password_reset object
        temp_key = self.cleaned_data.get("temp_key")
        password_reset = PasswordReset.objects.get(temp_key__exact=temp_key)
        
        # now set the new user password
        user = User.objects.get(passwordreset__exact=password_reset)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        user.message_set.create(message=ugettext(u"Password successfully changed."))
        
        # change all the password reset records to this person to be true.
        for password_reset in PasswordReset.objects.filter(user=user):
            password_reset.reset = True
            password_reset.save()


class ChangeTimezoneForm(AccountForm):
    
    timezone = TimeZoneField(label=_("Timezone"), required=True)
    
    def __init__(self, *args, **kwargs):
        super(ChangeTimezoneForm, self).__init__(*args, **kwargs)
        self.initial.update({"timezone": self.account.timezone})
    
    def save(self):
        self.account.timezone = self.cleaned_data["timezone"]
        self.account.save()
        self.user.message_set.create(message=ugettext(u"Timezone successfully updated."))


class ChangeLanguageForm(AccountForm):
    
    language = forms.ChoiceField(label=_("Language"), required=True, choices=settings.LANGUAGES)
    
    def __init__(self, *args, **kwargs):
        super(ChangeLanguageForm, self).__init__(*args, **kwargs)
        self.initial.update({"language": self.account.language})
    
    def save(self):
        self.account.language = self.cleaned_data["language"]
        self.account.save()
        self.user.message_set.create(message=ugettext(u"Language successfully updated."))


# @@@ these should somehow be moved out of account or at least out of this module

from account.models import OtherServiceInfo, other_service, update_other_services

class TwitterForm(UserForm):
    username = forms.CharField(label=_("Username"), required=True)
    password = forms.CharField(label=_("Password"), required=True,
                               widget=forms.PasswordInput(render_value=False))
    
    def __init__(self, *args, **kwargs):
        super(TwitterForm, self).__init__(*args, **kwargs)
        self.initial.update({"username": other_service(self.user, "twitter_user")})
    
    def save(self):
        from microblogging.utils import get_twitter_password
        update_other_services(self.user,
            twitter_user = self.cleaned_data['username'],
            twitter_password = get_twitter_password(settings.SECRET_KEY, self.cleaned_data['password']),
        )
        self.user.message_set.create(message=ugettext(u"Successfully authenticated."))
