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
from external.excel_response import ExcelResponse


from events.models import Event, Member
from events.forms import EventForm, QuestionsForm


def events_widget(request, template_name = "homepage.html"):

    events = Event.objects.order_by("-date")
    
    return render_to_response(template_name, {
        "events": events,
        }, context_instance=RequestContext(request))




@login_required
def map(request, template_name="events/map.html"):
    return render_to_response(template_name)


@login_required
def destroy(request, id):
    """
    latest ivents
    """
    event = Event.objects.get(id = id)
    event.members.all().delete()
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
def add_event(request, form_class=EventForm, template_name="events/add_event.html"):
    """
    upload form for photos
    """
    event_form = form_class(request.user)
    
    if request.method == 'POST':
        if request.POST.get("action") == "add":
            event_form = form_class(request.user, request.POST)

            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.creator = request.user
                event.save()
                event_member = Member(user=request.user)
                event_member.save()
                event.members.add(event_member)
                include_kwargs = {"id": event.id}
                redirect_to = reverse("event_details", kwargs=include_kwargs)
                return HttpResponseRedirect(redirect_to)
            
    return render_to_response(template_name, {
        "event_form": event_form
    }, context_instance=RequestContext(request))


@login_required
def edit(request, id, form_class=EventForm, template_name="events/edit.html"):
    """
    upload form for photos
    """
    event = get_object_or_404(Event, id=id)
    event_form = form_class(request.user, instance=event)
    if request.method == "POST":
        if request.POST["action"] == "update":
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
    latest ivents
    """
    events = Event.objects.order_by("-date")
    
    return render_to_response(template_name, {
        "events": events,
        }, context_instance=RequestContext(request))


@login_required
def join(request, id, form_class=QuestionsForm, template_name="events/questions.html"):

    event = get_object_or_404(Event, id=id)
    
    include_kwargs = {"id": event.id}
    redirect_to = reverse("event_details", kwargs=include_kwargs)   
        
    try:
        member = event.members.get(user = request.user)
    except ObjectDoesNotExist: # if user isn't member
        member = Member(user = request.user)
        if event.questions == "":
            member.save()

            event.members.add(member)
            event.save()
        else:
            questions_form = form_class(member)
            questions_form.setQuestions(event.questions)
            
            if request.method == "POST":
                questions_form.setData(request.POST)
                if questions_form.is_valid():
                    questions_form.save()
                    
                    event.members.add(member)
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
    
@login_required
def answers(request, id, template_name="events/answers.html"):
    event = get_object_or_404(Event, id=id)
    
    include_kwargs = {"id": event.id}
    redirect_to = reverse("event_details", kwargs=include_kwargs)
    
    if request.user != event.creator:
        return HttpResponseRedirect(redirect_to)
        
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
    
    include_kwargs = {"id": event.id}
    redirect_to = reverse("event_details", kwargs=include_kwargs)
    
    if request.user != event.creator:
        return HttpResponseRedirect(redirect_to)
        
    if request.method == "POST" and request.POST.get('action') == "delete":
        try:
            member = event.members.get(id = request.POST.get('member'))
            event.members.remove(member)
            member.delete()
            request.user.message_set.create(message=_(u"Учасника %s видалено з події.") % member)
            
        except ObjectDoesNotExist: # if user isn't member
            pass
        
    return render_to_response(template_name, {
        "event": event,
    }, context_instance=RequestContext(request))
