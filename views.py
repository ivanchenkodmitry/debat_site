# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, get_host
from django.template import RequestContext
from django.db.models import Q
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from blog.models import Post

from events.models import Event

def homepage_view (request, template_name = "homepage.html"):
        
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
