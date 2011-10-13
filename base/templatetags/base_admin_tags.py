from django import template
from django.conf import settings

register = template.Library()

def is_app_shown(value):
    if value['name'].lower() in settings.EXCLUDED_APPS_FROM_ADMIN :
        return False
    return True

register.filter('is_app_shown', is_app_shown)
