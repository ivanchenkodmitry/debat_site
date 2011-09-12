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

from photologue.models import *
from photos.models import UserGallery, UserPhoto
from photos.forms import PhotoUploadForm, PhotoEditForm, PhotoSetForm

                

def photos_widget(request, template_name = "homepage.html"):

    photos = Image.objects.order_by("-date")
    
    return render_to_response(template_name, {
        "photos": photos,
        }, context_instance=RequestContext(request))

                
def galleries(request, username=None, template_name="photos.html"):
    galleries = UserGallery.objects.order_by("-publish")
    if username is not None:
        user = get_object_or_404(User, username=username.lower())
        galleries = galleries.filter(author=user)
    return render_to_response(template_name, {
        "galleries": galleries,
    }, context_instance=RequestContext(request))
    
@login_required
def new(request, form_class=UserGalleryForm, template_name="photos/new.html"):
    if request.method == "POST":
        if request.POST["action"] == "create":
            gallery_form = form_class(request.user, request.POST)
            if gallery_form.is_valid():
                gallery = gallery_form.save(commit=False)
                gallery.author = request.user
                gallery.save()
                # Add uploaded photos to galleries
                gallery.photos.add(*blog_form.photos)
                gallery.save()
                
               
                return HttpResponseRedirect(reverse("gallery_list_yours"))
        else:
            gallery_form = form_class()
    else:
        gallery_form = form_class()
        
    
    photo_form = PhotoForm()

    return render_to_response(template_name, {
        "gallery_form": blog_form,
        "photo_form": photo_form,
    }, context_instance=RequestContext(request))
