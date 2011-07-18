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

from photologue.models import *
from events.models import Event
from photos.forms import PhotoUploadForm, PhotoEditForm


@login_required
def add_event(request, template_name="events/add_event.html"):
    """
    upload form for photos
    """
    
    if request.method == 'POST':
	if request.POST.get("action") == "Add":
		new_event = Event()
		new_event.title = request.POST.get("title")
		new_event.description = request.POST.get("description")
		new_event.date = request.POST.get("date")
		new_event.address = request.POST.get("address")
		new_event.creator = request.user.username
		new_event.save()
		
        	return render_to_response('events/latest.html', context_instance=RequestContext(request))

    return render_to_response(template_name, context_instance=RequestContext(request))



@login_required
def events(request, template_name="events/latest.html"):
    """
    latest ivents
    """
    events = Event.objects.order_by("title")
    
    return render_to_response(template_name, {
    "events": events,
    }, context_instance=RequestContext(request))
















