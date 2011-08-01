# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',


    # all clubs
    url(r'^$', 'clubs.views.clubs', name="clubs"),
    # Add club
    url(r'^add_club/$', 'clubs.views.add_club', name="add_club"),
    # a club details
    url(r'^details/(?P<id>\d+)/$', 'clubs.views.details', name="club_details"),
    url(r'^destroy/(?P<id>\d+)/$', 'clubs.views.destroy', name='club_destroy'),
    #edit club
    url(r'^edit/(?P<id>\d+)/$', 'clubs.views.edit', name='club_edit'),
   #join club
    url(r'^join/(?P<id>\d+)/$', 'clubs.views.join', name='club_join'),
    #leave club
    url(r'^leave/(?P<id>\d+)/$', 'clubs.views.leave', name='club_leave'),
    # Map
    url(r'^map/$', 'clubs.views.map', name="map"),
)
