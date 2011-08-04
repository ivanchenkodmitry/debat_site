# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator

from blog.models import Post

def homepage_view (request, template_name = "homepage.html"):
        
	adminposts = Post.objects.filter(status2=1).order_by("-publish")[0:4]
        posts = Post.objects.filter(status2=1).order_by("-publish")[0:7]
        


	return render_to_response(template_name, {
		"adminposts": adminposts, "posts":posts,
		}, context_instance=RequestContext(request))