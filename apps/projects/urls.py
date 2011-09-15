# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from projects import views, models



urlpatterns = patterns('',
    # blog post
    url(r'^details/(?P<id>\d+)/$', 'projects.views.project', name="project"),

    # all blog posts
    url(r'^$', 'projects.views.projects', name="projects_list_all"),

    # blog post for user
    # url(r'^posts/(?P<username>\w+)/$', 'blog.views.blogs', name='blog_list_user'),

    
    
    #preadd photo to post
    #url(r'^upload/photo$', 'projects.views.upload_photo'),
    )