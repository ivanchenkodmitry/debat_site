# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',


    # all 
    url(r'^$', 'universities.views.universities', name="universities"),
    # Add 
    url(r'^add_university/$', 'universities.views.add_university', name="add_university"),
   )