# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from blog.models import Post

from events.models import Event

def homepage_view (request, template_name = "homepage.html"):
        
        adminposts = Post.objects.filter(author__is_staff=True, status2=1).order_by("-publish")
        posts = Post.objects.filter(author__is_staff=False, status2=1).order_by("-publish")
        
	events = Event.objects.order_by("title")       

	return render_to_response(template_name, {
		"adminposts": adminposts,
		'posts':posts,
		'events': events,
		}, context_instance=RequestContext(request))

