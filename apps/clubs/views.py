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
from universities.models import University
from clubs.forms import *




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



@login_required
def details(request, id, template_name="clubs/details.html"):

	club = Club.objects.get(id = id)
	
	is_me = False
	is_member = False

	if request.user == club.admin:
		is_me = 'True'

	members = club.members.filter(approved=True)
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


@login_required
def add_club(request, form_class=ClubForm, template_name="clubs/add_club.html"):
    club_form = form_class(request.user)
    if request.method == "POST":
        if request.POST["action"] == "create":
            club_form = form_class(request.user, request.POST)
            
            if club_form.is_valid():
                club = club_form.save(commit=False)
                
                club.save()
                return HttpResponseRedirect(reverse("clubs"))
    return render_to_response(template_name, {
        "club_form": club_form
    }, context_instance=RequestContext(request))
        


@login_required
def edit(request, id, form_class=ClubForm,template_name="clubs/edit.html"):
    club = get_object_or_404(Club, id=id)
    club_form = form_class(request.user, instance=club)
    if request.method == "POST":
      if request.POST["action"] == "update":
	club_form = form_class(request.user, request.POST, instance=club)
	if club_form.is_valid():
                club = club_form.save(commit=False)
                club.save()
                return HttpResponseRedirect(reverse("clubs"))
    
                
    return render_to_response(template_name, {
        "club_form": club_form,
        "club": club,
    }, context_instance=RequestContext(request))


#@login_required
def clubs(request, template_name="clubs/clubs.html"):
	
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


	return HttpResponseRedirect('/clubs/newmember/')



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
