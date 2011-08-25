# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import models

from account.utils import get_default_redirect
from account.models import OtherServiceInfo
from account.forms import SignupForm, AddEmailForm, LoginForm, \
    ChangePasswordForm, SetPasswordForm, ResetPasswordForm, \
    ChangeTimezoneForm, ChangeLanguageForm, TwitterForm, ResetPasswordKeyForm
from emailconfirmation.models import EmailAddress, EmailConfirmation

from django.conf import settings as global_settings
import vkontakte
from django.utils import simplejson
from django.http import HttpResponse
from django.http import QueryDict
from django.core.urlresolvers import reverse

from profiles.models import Profile
import md5

association_model = models.get_model('django_openid', 'Association')
if association_model is not None:
    from django_openid.models import UserOpenidAssociation

def login(request, form_class=LoginForm, template_name="account/login.html",
          success_url=None, associate_openid=False, openid_success_url=None,
          url_required=False, extra_context=None):
    if extra_context is None:
        extra_context = {}
    if success_url is None:
        success_url = get_default_redirect(request)
    if request.method == "POST" and not url_required:
        form = form_class(request.POST)
        if form.login(request):
            if associate_openid and association_model is not None:
                for openid in request.session.get('openids', []):
                    assoc, created = UserOpenidAssociation.objects.get_or_create(
                        user=form.user, openid=openid.openid
                    )
                success_url = openid_success_url or success_url
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    ctx = {
        "form": form,
        "url_required": url_required,
    }
    ctx.update(extra_context)
    return render_to_response(template_name, ctx,
        context_instance = RequestContext(request)
    )

def signup(request, form_class=SignupForm,
        template_name="account/signup.html", success_url=None):

    if success_url is None:
        success_url = get_default_redirect(request)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            username, password = form.save()
            if settings.ACCOUNT_EMAIL_VERIFICATION:
                return render_to_response("account/verification_sent.html", {
                    "email": form.cleaned_data["email"],
                }, context_instance=RequestContext(request))
            else:
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                request.user.message_set.create(
                    message=_("Successfully logged in as %(username)s.") % {
                    'username': user.username
                })
                return HttpResponseRedirect(success_url)
    else:
        form = form_class()


    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))


def vk_data(request):

	success = True
	vk_cookie = request.COOKIES['vk_app_%s' % global_settings.VKONTAKTE_API_KEY]
	vk_query = QueryDict(vk_cookie)
	vk_id = vk_query['mid'] # Here we obtain the user id
        # After that check if user with this id exits
	
	vk = vkontakte.API(global_settings.VKONTAKTE_API_KEY, global_settings.VKONTAKTE_SECRET_KEY)

	user_vk_profile = vk.getProfiles(uids = vk_id, fields = 'uid, first_name, last_name, nickname, domain, sex, bdate, city, country, timezone, photo, photo_medium, photo_big, has_mobile, rate, contacts, education')[0]
	
	surname = user_vk_profile['last_name']
	name = user_vk_profile['first_name']
	birth_date = user_vk_profile['bdate']
	website = u'http://vk.com/' + user_vk_profile['domain']
	education = user_vk_profile['university_name'] + u', факультет '+ user_vk_profile['faculty_name'] + u' год окончания: ' + user_vk_profile['graduation']
	photo = user_vk_profile['photo_big']

	return HttpResponse(simplejson.dumps({
				'success': success,
				'vk_id' : vk_id,
				'surname' : surname,
				'name' : name,
				'birth_date' : birth_date,
				'website' : website,
				'education' : education,
				'photo' : photo,
				}))
	

def vk_login(request):
	success = True
	vk_cookie = request.COOKIES['vk_app_%s' % global_settings.VKONTAKTE_API_KEY]
	vk_query = QueryDict(vk_cookie)
	vk_id = vk_query['mid'] # Here we obtain the user id
        # After that check if user with this id exits
	
	user = authenticate(vk_id=vk_id)
	if user:
		redirect = '/'
		auth_login(request, user)
		request.user.message_set.create( message=_(u"Успішний логін %(first_name)s %(last_name)s") % {
						'first_name': user.get_profile().surname,
						'last_name': user.get_profile().name,
							 })
	else:
		redirect = '/account/signup/'
	return HttpResponse(simplejson.dumps({
				'success': success,
				'redirect': redirect,
				'vk_id' : vk_id,
				}))


def confirm_profile(request, profile_hash, template_name="account/confirm_profile.html"):
	try:
		profile = Profile.objects.get(md5_name = profile_hash)
		if not profile.user.is_active:
			profile.user.is_active = True
			profile.user.save()
	except:
		profile = None

	return render_to_response(template_name, {
        "profile": profile,
    }, context_instance=RequestContext(request))
	
	

@login_required
def email(request, form_class=AddEmailForm,
        template_name="account/email.html"):
    if request.method == "POST" and request.user.is_authenticated():
        if request.POST["action"] == "add":
            add_email_form = form_class(request.user, request.POST)
            if add_email_form.is_valid():
                add_email_form.save()
                add_email_form = form_class() # @@@
        else:
            add_email_form = form_class()
            if request.POST["action"] == "send":
                email = request.POST["email"]
                try:
                    email_address = EmailAddress.objects.get(
                        user=request.user,
                        email=email,
                    )
                    request.user.message_set.create(
                        message=_("Confirmation email sent to %(email)s") % {
                            'email': email,
                        })
                    EmailConfirmation.objects.send_confirmation(email_address)
                except EmailAddress.DoesNotExist:
                    pass
            elif request.POST["action"] == "remove":
                email = request.POST["email"]
                try:
                    email_address = EmailAddress.objects.get(
                        user=request.user,
                        email=email
                    )
                    email_address.delete()
                    request.user.message_set.create(
                        message=_("Removed email address %(email)s") % {
                            'email': email,
                        })
                except EmailAddress.DoesNotExist:
                    pass
            elif request.POST["action"] == "primary":
                email = request.POST["email"]
                email_address = EmailAddress.objects.get(
                    user=request.user,
                    email=email,
                )
                email_address.set_as_primary()
    else:
        add_email_form = form_class()
    return render_to_response(template_name, {
        "add_email_form": add_email_form,
    }, context_instance=RequestContext(request))

@login_required
def password_change(request, form_class=ChangePasswordForm,
        template_name="account/password_change.html"):
    if not request.user.password:
        return HttpResponseRedirect(reverse("acct_passwd_set"))
    if request.method == "POST":
        password_change_form = form_class(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            password_change_form = form_class(request.user)
    else:
        password_change_form = form_class(request.user)
    return render_to_response(template_name, {
        "password_change_form": password_change_form,
    }, context_instance=RequestContext(request))

@login_required
def password_set(request, form_class=SetPasswordForm,
        template_name="account/password_set.html"):
    if request.user.password:
        return HttpResponseRedirect(reverse("acct_passwd"))
    if request.method == "POST":
        password_set_form = form_class(request.user, request.POST)
        if password_set_form.is_valid():
            password_set_form.save()
            return HttpResponseRedirect(reverse("acct_passwd"))
    else:
        password_set_form = form_class(request.user)
    return render_to_response(template_name, {
        "password_set_form": password_set_form,
    }, context_instance=RequestContext(request))

@login_required
def password_delete(request, template_name="account/password_delete.html"):
    # prevent this view when openids is not present or it is empty.
    if not request.user.password or \
        (not hasattr(request, "openids") or \
            not getattr(request, "openids", None)):
        return HttpResponseForbidden()
    if request.method == "POST":
        request.user.password = u""
        request.user.save()
        return HttpResponseRedirect(reverse("acct_passwd_delete_done"))
    return render_to_response(template_name, {
    }, context_instance=RequestContext(request))

def password_reset(request, form_class=ResetPasswordForm,
        template_name="account/password_reset.html",
        template_name_done="account/password_reset_done.html"):
    if request.method == "POST":
        password_reset_form = form_class(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.save()
            return render_to_response(template_name_done, {
                "email": email,
            }, context_instance=RequestContext(request))
    else:
        password_reset_form = form_class()
    
    return render_to_response(template_name, {
        "password_reset_form": password_reset_form,
    }, context_instance=RequestContext(request))
    
def password_reset_from_key(request, key, form_class=ResetPasswordKeyForm,
        template_name="account/password_reset_from_key.html"):
    if request.method == "POST":
        password_reset_key_form = form_class(request.POST)
        if password_reset_key_form.is_valid():
            password_reset_key_form.save()
            password_reset_key_form = None
    else:
        password_reset_key_form = form_class(initial={"temp_key": key})
    
    return render_to_response(template_name, {
        "form": password_reset_key_form,
    }, context_instance=RequestContext(request))
    
@login_required
def timezone_change(request, form_class=ChangeTimezoneForm,
        template_name="account/timezone_change.html"):
    if request.method == "POST":
        form = form_class(request.user, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = form_class(request.user)
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))

@login_required
def language_change(request, form_class=ChangeLanguageForm,
        template_name="account/language_change.html"):
    if request.method == "POST":
        form = form_class(request.user, request.POST)
        if form.is_valid():
            form.save()
            next = request.META.get('HTTP_REFERER', None)
            return HttpResponseRedirect(next)
    else:
        form = form_class(request.user)
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))

@login_required
def other_services(request, template_name="account/other_services.html"):
    from microblogging.utils import twitter_verify_credentials
    twitter_form = TwitterForm(request.user)
    twitter_authorized = False
    if request.method == "POST":
        twitter_form = TwitterForm(request.user, request.POST)

        if request.POST['actionType'] == 'saveTwitter':
            if twitter_form.is_valid():
                from microblogging.utils import twitter_account_raw
                twitter_account = twitter_account_raw(
                    request.POST['username'], request.POST['password'])
                twitter_authorized = twitter_verify_credentials(
                    twitter_account)
                if not twitter_authorized:
                    request.user.message_set.create(
                        message=ugettext("Twitter authentication failed"))
                else:
                    twitter_form.save()
    else:
        from microblogging.utils import twitter_account_for_user
        twitter_account = twitter_account_for_user(request.user)
        twitter_authorized = twitter_verify_credentials(twitter_account)
        twitter_form = TwitterForm(request.user)
    return render_to_response(template_name, {
        "twitter_form": twitter_form,
        "twitter_authorized": twitter_authorized,
    }, context_instance=RequestContext(request))

@login_required
def other_services_remove(request):
    # TODO: this is a bit coupled.
    OtherServiceInfo.objects.filter(user=request.user).filter(
        Q(key="twitter_user") | Q(key="twitter_password")
    ).delete()
    request.user.message_set.create(message=ugettext("Removed twitter account information successfully."))
    return HttpResponseRedirect(reverse("acct_other_services"))
