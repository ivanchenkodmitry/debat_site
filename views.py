# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from blog.models import Post

from events.models import Event
from photos.models import Image, Pool
#import random
from datetime import datetime

def homepage_view (request, template_name = "homepage.html"):
        
    adminposts = Post.objects.filter(author__is_staff=True, status2=1).order_by("-publish")
    posts = Post.objects.filter(author__is_staff=False, status2=1).order_by("-publish")

    users = User.objects.all()    
    events = Event.objects.filter(approved=True).order_by("-date_begin")
    nearest_events = events.filter(date_begin__gte=datetime.now())

    if nearest_events:
        _nearest_event = nearest_events[0]
        nearest_event = list(events).index(_nearest_event)
    else:
        nearest_event = None
    
    rand_photos = Image.objects.order_by('?')
        
    return render_to_response(template_name, {
        'adminposts': adminposts,
        'posts':posts,
        'events': events,
        'nearest_event': nearest_event,
        'rand_photo': rand_photos,
	'users': users,
        }, context_instance=RequestContext(request))

