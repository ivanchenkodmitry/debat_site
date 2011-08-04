# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator

from blog.models import Post

from events.models import Event

def homepage_view (request, template_name = "homepage.html"):
        
<<<<<<< HEAD
	posts = Post.objects.filter(status2=1).order_by("-publish")
        paginator = Paginator(posts, 3)
		
        adminposts = Post.objects.filter(status2=1).order_by("-publish")
        adminpaginator = Paginator(adminposts, 3)

        
	events = Event.objects.order_by("title")       

	return render_to_response(template_name, {
		"adminposts": adminposts,
		'posts':posts,
		'events': events,
		}, context_instance=RequestContext(request))
=======
	adminposts = Post.objects.filter(status2=1).order_by("-publish")[0:4]
        posts = Post.objects.filter(status2=1).order_by("-publish")[0:7]
        


	return render_to_response(template_name, {
		"adminposts": adminposts, "posts":posts,
		}, context_instance=RequestContext(request))
>>>>>>> bogdan_dev
