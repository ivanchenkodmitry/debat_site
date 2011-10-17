# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # all photos or latest photos
    url(r'^$', 'photos.views.photos', name = "photos"),
    # a photos details
    url(r'^details/(?P<id>\d+)/$', 'photos.views.details', name = "photo_details"),
    # upload photos
    url(r'^upload/$', 'photos.views.upload', name = "photo_upload"),
    # your photos
    url(r'^yourphotos/$', 'photos.views.yourphotos', name = 'photos_yours'),
    # a members photos
    url(r'^member/(?P<username>[\w]+)/$', 'photos.views.memberphotos', name = 'photos_member'),
    #destory photo
    url(r'^destroy/(?P<id>\d+)/(?P<photoset_id>\d+)$', 'photos.views.destroy', name = 'photo_destroy'),
    #edit photo
    url(r'^edit/(?P<id>\d+)/$', 'photos.views.edit', name = 'photo_edit'),

    #Create Gallery
    url(r'^new/photoset/$', 'photos.views.newphotoset', name = 'newphotoset'),

    url(r'^photoset/$', 'photos.views.photosets', name = 'photoset'),

    url(r'^photoset/(?P<id>\d+)/$', 'photos.views.photoset'),

    url(r'^edit/photoset/(?P<id>\d+)/$', 'photos.views.editphotoset'),

    url(r'^add/to/photoset/(?P<id>\d+)/$', 'photos.views.add_to_photoset'),

    # myphotosets
    url(r'^myphotosets/$', 'photos.views.myphotosets', name = 'myphotosets'),
# recent photos
    url(r'^recentphotos/$', 'photos.views.recentphotos', name = 'recentphotos'),

)
