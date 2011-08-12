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

from universities.models import University
from universities.forms import *

    
def universities(request, template_name="universities/universities.html"):
	
	universities = University.objects.order_by("title")
    
	return render_to_response(template_name, {
		"universities": universities,
		}, context_instance=RequestContext(request))
		
		
@login_required
def add_university(request, form_class=UniversityForm, template_name="universities/add_university.html"):
    university_form = form_class(request.user)
    if request.method == "POST":
        if request.POST["action"] == "create":
            university_form = form_class(request.user, request.POST)
            
            if university_form.is_valid():
                university = university_form.save(commit=False)
                university.save()
                return HttpResponseRedirect(reverse("universities"))
    return render_to_response(template_name, {
        "university_form": university_form
    }, context_instance=RequestContext(request))


    

'''@login_required
def details(request, title, template_name="universities/details.html"):

	university = University.objects.get(title = title)
	
	return render_to_response(template_name, {
    "university": university,
	
    }, context_instance=RequestContext(request))'''
    
    

'''def edit(request, id, form_class=UniversityForm,template_name="universities/edit.html"):
    university = get_object_or_404(Club, id=id)
    university_form = form_class(request.user, instance=university)
    if request.method == "POST":
      if request.POST["action"] == "update":
	university_form = form_class(request.user, instance=university)
	if university_form.is_valid():
                university = university_form.save(commit=False)
                university.save()
                return HttpResponseRedirect(reverse("universities"))
    
                
    return render_to_response(template_name, {
        "university_form": university_form,
        "university": university,
    }, context_instance=RequestContext(request))'''    