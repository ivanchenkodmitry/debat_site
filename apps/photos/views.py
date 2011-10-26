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
from photos.models import Image, Pool, PhotoSet
from photos.forms import PhotoUploadForm, PhotoEditForm, PhotoSetForm


@login_required
def upload(request, form_class = PhotoUploadForm,
        template_name = "photos/upload.html", group_slug = None, bridge = None):
    """
    upload form for photos
    """

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    photo_form = form_class()
    if request.method == 'POST':
        if request.POST.get("action") == "upload":
            photo_form = form_class(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit = False)
                photo.member = request.user
                photo.save()

                # in group context we create a Pool object for it
                if group:
                    pool = Pool()
                    pool.photo = photo
                    group.associate(pool)
                    pool.save()

                request.user.message_set.create(message = _("Successfully uploaded photo '%s'") % photo.title)

                include_kwargs = {"id": photo.id}
                if group:
                    redirect_to = bridge.reverse("photo_details", group, kwargs = include_kwargs)
                else:
                    redirect_to = reverse("photo_details", kwargs = include_kwargs)

                return HttpResponseRedirect(redirect_to)

    return render_to_response(template_name, {
        "group": group,
        "photo_form": photo_form,
    }, context_instance = RequestContext(request))


@login_required
def yourphotos(request, template_name = "photos/yourphotos.html", group_slug = None, bridge = None):
    """
    photos for the currently authenticated user
    """

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    photos = Image.objects.filter(member = request.user)

    if group:
        photos = group.content_objects(photos, join = "pool")
    else:
        photos = photos.filter(pool__object_id = None)

    photos = photos.order_by("-date_added")

    return render_to_response(template_name, {
        "group": group,
        "photos": photos,
    }, context_instance = RequestContext(request))


#@login_required
def photos(request, template_name = "photos/latest.html", group_slug = None, bridge = None):
    """
    latest photosets
    """

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    photosets = PhotoSet.objects.all()

    photosets = photosets.order_by("-date_added")

    return render_to_response(template_name, {
        "photosets": photosets,
    }, context_instance = RequestContext(request))



def details(request, id, template_name = "photos/details.html", group_slug = None, bridge = None):
    """
    show the photo details
    """

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    photos = Image.objects.all()

    if group:
        photos = group.content_objects(photos, join = "pool")
    else:
        photos = photos.filter(pool__object_id = None)

    photo = get_object_or_404(photos, id = id)

    # @@@: test
    if not photo.is_public and request.user != photo.member:
        raise Http404

    photo_url = photo.get_display_url()

    title = photo.title
    host = "http://%s" % get_host(request)

    if photo.member == request.user:
        is_me = True
    else:
        is_me = False

    return render_to_response(template_name, {
        "group": group,
        "host": host,
        "photo": photo,
        "photo_url": photo_url,
        "is_me": is_me,
    }, context_instance = RequestContext(request))


@login_required
def memberphotos(request, username, template_name = "photos/memberphotos.html", group_slug = None, bridge = None):
    """
    Get the members photos and display them
    """

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    user = get_object_or_404(User, username = username)

    photos = Image.objects.filter(
        member__username = username,
        is_public = True,
    )

    if group:
        photos = group.content_objects(photos, join = "pool")
    else:
        photos = photos.filter(pool__object_id = None)

    photos = photos.order_by("-date_added")

    return render_to_response(template_name, {
        "group": group,
        "photos": photos,
    }, context_instance = RequestContext(request))


@login_required
def edit(request, id, form_class = PhotoEditForm,
        template_name = "photos/edit.html", group_slug = None, bridge = None):

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    photos = Image.objects.all()

    if group:
        photos = group.content_objects(photos, join = "pool")
    else:
        photos = photos.filter(pool__object_id = None)

    photo = get_object_or_404(photos, id = id)
    photo_url = photo.get_display_url()

    if request.method == "POST":
        if photo.member != request.user:
            request.user.message_set.create(message = "You can't edit photos that aren't yours")

            include_kwargs = {"id": photo.id}
            if group:
                redirect_to = bridge.reverse("photo_details", group, kwargs = include_kwargs)
            else:
                redirect_to = reverse("photo_details", kwargs = include_kwargs)

            return HttpResponseRedirect(reverse('photo_details', args = (photo.id,)))
        if request.POST["action"] == "update":
            photo_form = form_class(request.user, request.POST, instance = photo)
            if photo_form.is_valid():
                photoobj = photo_form.save(commit = False)
                photoobj.save()

                request.user.message_set.create(message = _("Successfully updated photo '%s'") % photo.title)

                include_kwargs = {"id": photo.id}
                if group:
                    redirect_to = bridge.reverse("photo_details", group, kwargs = include_kwargs)
                else:
                    redirect_to = reverse("photo_details", kwargs = include_kwargs)

                return HttpResponseRedirect(redirect_to)
        else:
            photo_form = form_class(instance = photo)

    else:
        photo_form = form_class(instance = photo)

    return render_to_response(template_name, {
        "group": group,
        "photo_form": photo_form,
        "photo": photo,
        "photo_url": photo_url,
    }, context_instance = RequestContext(request))

@login_required
def destroy(request, id, photoset_id, group_slug = None, bridge = None):

    redirect_to = "/photos/edit/photoset/%s/" % photoset_id

    photo = get_object_or_404(Image, pk = id)
    title = photo.title

    if photo.member != request.user:
        request.user.message_set.create(message = "You can't delete photos that aren't yours")
        return HttpResponseRedirect(redirect_to)

    photo.delete()
    request.user.message_set.create(message = _("Successfully deleted photo '%s'") % title)

    return HttpResponseRedirect(redirect_to)


def newphotoset(request):
    if request.method == 'POST':
        photoset_form = PhotoSetForm(request.user, request.POST)
        if photoset_form.is_valid():
            photoset = photoset_form.save(commit = False)
            photoset.user = request.user
            photoset.save()
            redirect_to = "/photos/edit/photoset/%i" % photoset.pk
            return HttpResponseRedirect(redirect_to)
    else:
        photoset_form = PhotoSetForm()
    return render_to_response('photos/newphotoset.html', {'photoset_form': photoset_form}, context_instance = RequestContext(request))

def editphotoset(request, id):
    photo_form = PhotoUploadForm
    photoset = get_object_or_404(PhotoSet, id = id)
    photoset_form = PhotoSetForm (instance = photoset)

    if request.method == 'POST':
        if request.POST['action'] == 'addphoto':
            photo_form = PhotoUploadForm(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save()
                photo.member = request.user
                photo.photoset.add(photoset)
                photo.save()

        elif request.POST['action'] == 'editphotoset':
            photoset_form = PhotoSetForm(request.user, request.POST, instance = photoset)
            if photoset_form.is_valid():
                photoset = photoset_form.save(commit = False)
                
                photoset.save()
                
                redirect_to = "/photos/photoset/%i" % photoset.pk
                return HttpResponseRedirect(redirect_to)



    return render_to_response('photos/editphotoset.html', {'photo_form': photo_form,
                                                            'photoset_form': photoset_form,
                                                            
                                                            'photoset': photoset},
                                                            context_instance = RequestContext(request))

def photosets(request):
    pass

def photoset(request, id):
    photoset = get_object_or_404(PhotoSet, pk = id)
    return render_to_response('photos/photoset.html', {'photoset': photoset}, context_instance = RequestContext(request))

def add_to_photoset(request, id):
    photoset = get_object_or_404(PhotoSet, pk = id)
    photoset_form = PhotoSetForm()
    if request.method == 'POST':
        photo_form = PhotoUploadForm(request.user, request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit = False)
            photo.photoset.add(photoset)
            photo.save()
            return HttpResponseRedirect('/photos/edit/photoset/%s/' % photoset.pk)
    else:
        photo_form = PhotoUploadForm()
    return render_to_response('photos/editphotoset.html', {'photoset_form': photoset_form,
                                                            'photo_form': photo_form,
                                                            'photoset': photoset},
                                                            context_instance = RequestContext(request))

def myphotosets(request, template_name = "photos/myphotosets.html", group_slug = None, bridge = None):
    """
    my photosets
    """

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    photosets = PhotoSet.objects.filter(user=request.user)

    photosets = photosets.order_by("-date_added")

    return render_to_response(template_name, {
        "photosets": photosets,
    }, context_instance = RequestContext(request))




def recentphotos(request, template_name = "photos/recentphotos.html", group_slug = None, bridge = None):
    """
    photos
    """

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    photos = Image.objects.all()

    if group:
        photos = group.content_objects(photos, join = "pool")
    else:
        photos = photos.filter(pool__object_id = None)

    photos = photos.order_by("-date_added")

    return render_to_response(template_name, {
        "group": group,
        "photos": photos,
    }, context_instance = RequestContext(request))

    
