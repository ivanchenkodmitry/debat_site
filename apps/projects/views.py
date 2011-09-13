# -*- coding: utf-8 -*-
import datetime, time
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.views.generic import date_based
from django.conf import settings
from photologue.models import Photo, Gallery
from pytils.translit import slugify


from projects.models import Project




def projects(request, username=None, template_name="projects/projects.html"):
    projects = Project.objects.order_by("-created_at")
    return render_to_response(template_name, {
        "projects": projects,
    }, context_instance=RequestContext(request))
    

def project(request, id,
         template_name="projects/details.html"):
    project = Project.objects.get(id=id)
    if not project:
        raise Http404

    return render_to_response(template_name, {
        "project": project,
    }, context_instance=RequestContext(request))



'''def upload_photo(request):
    photo_title = "photo_title_%.20f" % time.time()
    photo_title = photo_title.replace('.', '_')
    photo_form = PhotoForm(request.POST, request.FILES)
    if photo_form.is_valid():
        photo = photo_form.save(commit = False)
        photo.title = photo_title
        photo.title_slug = photo_title
        photo.save()
        callback_script = "window.top.window.stopUpload(0, %s, '%s');" % (photo.id, photo.get_thumbnail_url())
    else:
        callback_script = "window.top.window.stopUpload(1);";
    response = <!DOCTYPE HTML>
        <html>
        <head></head>
        <body>
            <script language="javascript" type="text/javascript">
               %s
            </script>
        </body>
        </html>   
     % callback_script
    
    return HttpResponse(response)'''
