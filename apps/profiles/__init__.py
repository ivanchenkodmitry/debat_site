from django import template
from django.conf import settings

register = template.Library()

def is_app_shown(value, arg):
    import pdb; pdb.set_trace()

register.filter('is_app_shown', is_app_shown)

