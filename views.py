# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from blog.models import Post

from events.models import Event
from photos.models import Image, Pool
import random

def homepage_view (request, template_name = "homepage.html"):
        
    adminposts = Post.objects.filter(author__is_staff=True, status2=1).order_by("-publish")
    posts = Post.objects.filter(author__is_staff=False, status2=1).order_by("-publish")
        
    events = Event.objects.filter(approved=True).order_by("title")

    photo = Image.objects.all()
    photo = photo[random.randint(0, (photo.__len__() -1))]
    


    return render_to_response(template_name, {
		"adminposts": adminposts,
		'posts':posts,
		'events': events,
        'photo': photo,
		}, context_instance=RequestContext(request))

