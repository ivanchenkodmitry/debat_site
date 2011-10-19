# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, get_host
from django.template import RequestContext
from django.db.models import Q
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from external.excel_response import ExcelResponse
from photos.models import PhotoSet

from events.models import Event, AnswerList
from events.forms import EventForm, QuestionsForm


def events_widget(request, template_name = "homepage.html"):

    events = Event.objects.filter(approved=True).order_by("-date")
    
    return render_to_response(template_name, {
        "events": events,
        }, context_instance=RequestContext(request))




@login_required
def map(request, template_name="events/map.html"):
    return render_to_response(template_name)


@login_required
def destroy(request, id):
    """
    Delete event
    """
    event = get_object_or_404(Event, id=id)
    event.delete()

    redirect_to = reverse("events")

    return HttpResponseRedirect(redirect_to)



#@login_required
def details(request, id, template_name="events/details.html"):

    event = get_object_or_404(Event, id=id)
    
    if event.creator == request.user:
        is_me = True
    else:
        is_me = False
        
    is_member = event.user_is_member(request.user)
        
    if (not event.approved) and (not is_me):
        raise Http404
    photoset = get_object_or_404(PhotoSet, pk =   event.gallery.id
)

    return render_to_response(template_name, {
    "event": event,
    "is_me": is_me,
    "is_member": is_member,
    "photoset": photoset,
    }, context_instance=RequestContext(request))


@login_required
def add_event(request, form_class=EventForm, template_name="events/add_event.html"):
    """
    Add new event
    """
    event_form = form_class(request.user)
    
    if request.method == 'POST' and request.POST.get("action") == "add":
        event_form = form_class(request.user, request.POST, request.FILES)

        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.creator = request.user
            photoset = PhotoSet(name = event.title, user = request.user)
            photoset.save()
                
            event.gallery = photoset
            event.approved = request.user.is_staff
            # automatically approved if user is an administrator
            event.save()
            event.members.add(request.user)
            event.save()
            photoset.content_object = event
            photoset.save()


            if not event.approved:
                request.user.message_set.create(message=_(u"Адміністратор розгляне вашу заявку."))
            include_kwargs = {"id": event.id}
            redirect_to = "/photos/edit/photoset/%i" % photoset.pk
            return HttpResponseRedirect(redirect_to)
        else:
            event_form = form_class()
    return render_to_response(template_name, {
        "event_form": event_form
    }, context_instance=RequestContext(request))


@login_required
def edit(request, id, form_class=EventForm, template_name="events/edit.html"):
    """
    Edit event
    """
    event = get_object_or_404(Event, id=id)
    
    event_form = form_class(request.user, instance=event)
    if request.method == "POST" and request.POST.get("action") == "update":
        event_form = form_class(request.user, request.POST, instance=event)
        if event_form.is_valid():
            event = event_form.save()
            
            include_kwargs = {"id": event.id}
            redirect_to = reverse("event_details", kwargs=include_kwargs)
            return HttpResponseRedirect(redirect_to)
                
    return render_to_response(template_name, {
        "event_form": event_form,
        "event": event,
    }, context_instance=RequestContext(request))


#@login_required
def events(request, template_name="events/latest.html"):
    """
    Latest ivents
    """
    events = Event.objects.filter(approved=True).order_by("-date")
    photosets = PhotoSet.objects.all()

    photosets = photosets.order_by("-date_added")

   
    return render_to_response(template_name, {
        "events": events,
        "photosets": photosets,
        }, context_instance=RequestContext(request))


@login_required
def your_events(request, template_name="events/your_events.html"):
    return render_to_response(template_name, {
        "events": Event.objects.filter(creator=request.user),
    }, context_instance=RequestContext(request))


@login_required
def join(request, id, form_class=QuestionsForm, template_name="events/questions.html"):

    event = get_object_or_404(Event, id=id)
    
    if not event.approved:
        raise Http404
    
    include_kwargs = {"id": event.id}
    redirect_to = reverse("event_details", kwargs=include_kwargs)
    
    if event.user_is_member(request.user):
        request.user.message_set.create(message=_(u"Ви вже є учасником цієї події"))
    else:
        if event.questions == "":
            event.members.add(request.user)
            event.save()
        else:
            questions_form = form_class(event, request.user)
            questions_form.setQuestions(event.questions)
            
            if request.method == "POST":
                questions_form.setData(request.POST)
                if questions_form.is_valid():
                    questions_form.save()
                    
                    event.members.add(request.user)
                    event.save()
                    return HttpResponseRedirect(redirect_to)
            
            return render_to_response(template_name, {
                "questions_form": questions_form,
                "event": event
            }, context_instance=RequestContext(request))
            
    return HttpResponseRedirect(redirect_to)

@login_required
def leave(request, id, template_name="events/details.html"):
    event = Event.objects.get(id = id)
    
    if event.creator != request.user:
        raise Http404
    
    if event.user_is_member(request.user):
        event.members.remove(request.user)
        try:
            answer_list = AnswerList.objects.get(event=event, user=request.user)
            answer_list.delete()
        except AnswerList.DoesNotExist:
            pass
 
    include_kwargs = {"id": event.id}
    redirect_to = reverse("event_details", kwargs=include_kwargs)
    return HttpResponseRedirect(redirect_to)
    
@login_required
def answers(request, id, template_name="events/answers.html"):
    event = get_object_or_404(Event, id=id)
    
    if event.creator != request.user:
        raise Http404
        
    if request.GET.get('action') == 'export':
        data = event.get_excel_data()
        return ExcelResponse(data, output_name='answers')
    
    table = event.get_table_data()
    
    return render_to_response(template_name, {
        "event": event,
        "table": table,
    }, context_instance=RequestContext(request))
    
@login_required
def members(request, id, template_name="events/members.html"):
    event = get_object_or_404(Event, id=id)
    
    if event.creator == request.user:
        is_me = True
    else:
        is_me = False

    if is_me and request.method == "POST" and request.POST.get('action') == "delete":
        try:
            member = User.objects.get(id = request.POST.get('member'))
            if event.user_is_member(member):
                event.members.remove(member)
                try:
                    answer_list = AnswerList.objects.get(event=event, user=member)
                    answer_list.delete()
                except AnswerList.DoesNotExist:
                    pass
                request.user.message_set.create(message=_(u"Учасника %s видалено з події.") % unicode(member.get_profile()))
        except User.DoesNotExist:
            pass
        
    return render_to_response(template_name, {
        "event": event,
        "is_me": is_me,
    }, context_instance=RequestContext(request))


def photoset(request, id):
    event = get_object_or_404(Event, id=id)
    pk = event.gallery.id
    photoset = get_object_or_404(PhotoSet, pk = pk)
    return render_to_response('events/details.html', {'photoset': photoset}, context_instance = RequestContext(request))

