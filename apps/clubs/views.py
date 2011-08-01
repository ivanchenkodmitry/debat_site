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


from clubs.models import Club
from clubs.models import Members




@login_required
def map(request, template_name="clubs/map.html"):
	return render_to_response(template_name)


@login_required
def destroy(request, id):
	"""
	latest ivents
	"""
	club = Club.objects.get(id = id)
	club.members.all().delete()
	club.delete()

	redirect_to = '/clubs/'

	return HttpResponseRedirect(redirect_to)



#@login_required
def details(request, id, template_name="clubs/details.html"):

	club = Club.objects.get(id = id)
	
	is_me = False
	is_member = False

	if request.user == club.admin:
		is_me = 'True'

	members = club.members.all()
	for member in members:
		if member.user == request.user:
			is_member = True
			break

    
	return render_to_response(template_name, {
    "club": club,
	"is_me": is_me,
	"is_member": is_member,
	"members": members,
    }, context_instance=RequestContext(request))


#@login_required
def add_club(request, template_name="clubs/add_club.html"):
    """
    upload form for photos
    """
    
    if request.method == 'POST':
		if request.POST.get("action") == "Add":
			new_club = Club()
			new_club.title = request.POST.get("title")
			new_club.university = request.POST.get("university")
			new_club.date = request.POST.get("date")
			new_club.address = request.POST.get("address")
			new_club.location = request.POST.get("location")
			new_club.admin = request.user
			new_club.save()

			member = Members()
			member.user = request.user
			member.save()

			new_club.members.add(member)
			new_club.save()
			
			include_kwargs = {"id": new_club.id}
			redirect_to = reverse("club_details", kwargs=include_kwargs)
			return HttpResponseRedirect(redirect_to)
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def edit(request, id, template_name="clubs/edit.html"):
    """
    upload form for photos
    """
    edit_club = Club.objects.get(id = id)
    if request.method == 'POST':
		if request.POST.get("action") == "Edit":
			edit_club.title = request.POST.get("title")
			edit_club.university = request.POST.get("university")
			edit_club.date = request.POST.get("date")
			edit_club.address = request.POST.get("address")
			edit_club.location = request.POST.get("location")
			edit_club.admin = request.user
			edit_club.save()
			
			include_kwargs = {"id": edit_club.id}
			redirect_to = reverse("club_details", kwargs=include_kwargs)
			return HttpResponseRedirect(redirect_to)
    return render_to_response(template_name, { 'club': edit_club }, context_instance=RequestContext(request))


#@login_required
def clubs(request, template_name="clubs.html"):
	
	clubs = Club.objects.order_by("title")
    
	return render_to_response(template_name, {
		"clubs": clubs,
		}, context_instance=RequestContext(request))


@login_required
def join(request, id, template_name="clubs/details.html"):

	club = Club.objects.get(id = id)
	
	members = club.members.all()
	is_member = False	

	for member in members:
		if member.user == request.user:
			is_member = True
			break	
		
	if is_member:
		pass
	else:
		member = Members()
		member.user = request.user
		member.save()

		club.members.add(member)
		club.save()

	include_kwargs = {"id": club.id}
	redirect_to = reverse("club_details", kwargs=include_kwargs)
	return HttpResponseRedirect(redirect_to)

@login_required
def leave(request, id, template_name="club/details.html"):
	club = Club.objects.get(id = id)
	
	members = club.members.all()

	is_member = True
	for member in members:
		if member.user == request.user:
			member.delete()
			member.save()
			break

	club.save()
	include_kwargs = {"id": club.id}
	redirect_to = reverse("club_details", kwargs=include_kwargs)
	return HttpResponseRedirect(redirect_to)



# Create your views here.
