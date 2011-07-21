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


from events.models import Event
from events.models import Member




@login_required
def map(request, template_name="events/map.html"):
	return render_to_response(template_name)


@login_required
def destroy(request, id):
    """
    latest ivents
    """
    event = Event.objects.get(id = id)
    event.delete()
    
    redirect_to = '/events/'

    return HttpResponseRedirect(redirect_to)



#@login_required
def details(request, id, template_name="events/details.html"):

	event = Event.objects.get(id = id)
	
	is_me = False
	is_member = False

	if request.user == event.creator:
		is_me = 'True'

	members = event.members.all()
	for member in members:
		if member.user == request.user:
			is_member = True
			break

    
	return render_to_response(template_name, {
    "event": event,
	"is_me": is_me,
	"is_member": is_member,
	"members": members,
    }, context_instance=RequestContext(request))


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
			new_event.location = request.POST.get("location")
			new_event.creator = request.user
			new_event.save()

			member = Member()
			member.user = request.user
			member.save()

			new_event.members.add(member)
			new_event.save()
			
			include_kwargs = {"id": new_event.id}
			redirect_to = reverse("event_details", kwargs=include_kwargs)
			return HttpResponseRedirect(redirect_to)
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def edit(request, id, template_name="events/edit.html"):
    """
    upload form for photos
    """
    edit_event = Event.objects.get(id = id)
    if request.method == 'POST':
		if request.POST.get("action") == "Edit":
			edit_event.title = request.POST.get("title")
			edit_event.description = request.POST.get("description")
			edit_event.date = request.POST.get("date")
			edit_event.address = request.POST.get("address")
			edit_event.location = request.POST.get("location")
			edit_event.creator = request.user
			edit_event.save()
			
			include_kwargs = {"id": edit_event.id}
			redirect_to = reverse("event_details", kwargs=include_kwargs)
			return HttpResponseRedirect(redirect_to)
    return render_to_response(template_name, { 'event': edit_event }, context_instance=RequestContext(request))


#@login_required
def events(request, template_name="events/latest.html"):
	"""
	latest ivents
	"""
	events = Event.objects.order_by("title")
    
	return render_to_response(template_name, {
		"events": events,
		}, context_instance=RequestContext(request))


@login_required
def join(request, id, template_name="events/details.html"):

	event = Event.objects.get(id = id)
	
	members = event.members.all()
	is_member = False	

	for member in members:
		if member.user == request.user:
			is_member = True
			break	
		
	if is_member:
		pass
	else:
		member = Member()
		member.user = request.user
		member.save()

		event.members.add(member)
		event.save()

	include_kwargs = {"id": event.id}
	redirect_to = reverse("event_details", kwargs=include_kwargs)
	return HttpResponseRedirect(redirect_to)

@login_required
def leave(request, id, template_name="events/details.html"):
	event = Event.objects.get(id = id)
	
	members = event.members.all()
	is_member = True
	for member in members:
		if member.user == request.user:
			member.delete()
			member.save()
			break

	event.save()
	include_kwargs = {"id": event.id}
	redirect_to = reverse("event_details", kwargs=include_kwargs)
	return HttpResponseRedirect(redirect_to)
	
	











