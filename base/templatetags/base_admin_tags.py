from django import template
from django.conf import settings

register = template.Library()

def is_app_shown(value):
    if value['name'].lower() in settings.EXCLUDED_APPS_FROM_ADMIN :
        return False
    return True

def is_even(value):
    if value % 2 == 0:
        return True
    return False

def shown_apps(app_list):
    retlist = []
    for app in app_list:
        if app['name'].lower() not in settings.EXCLUDED_APPS_FROM_ADMIN:
            retlist.append(app)
    return retlist


register.filter('is_app_shown', is_app_shown)
register.filter('is_even', is_even)
register.filter('shown_apps', shown_apps)
