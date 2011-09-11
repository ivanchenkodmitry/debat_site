from django.conf.urls.defaults import *

urlpatterns = patterns('',


    # all ivent or latest ivent
    url(r'^$', 'events.views.events', name="events"),
    # your events
    url(r'^your_events/$', 'events.views.your_events', name='event_list_yours'),
    # Add event
    url(r'^add_event/$', 'events.views.add_event', name="add_event"),
    # an event details
    url(r'^details/(?P<id>\d+)/$', 'events.views.details', name="event_details"),
    url(r'^destroy/(?P<id>\d+)/$', 'events.views.destroy', name='event_destroy'),
    #edit event
    url(r'^edit/(?P<id>\d+)/$', 'events.views.edit', name='event_edit'),
    #join to event
    url(r'^join/(?P<id>\d+)/$', 'events.views.join', name='event_join'),
    #leave event
    url(r'^leave/(?P<id>\d+)/$', 'events.views.leave', name='event_leave'),
    # Map
    url(r'^map/$', 'events.views.map', name="map"),
    #answers
    url(r'^answers/(?P<id>\d+)/$', 'events.views.answers', name='event_answers'),
    #member list
    url(r'^members/(?P<id>\d+)/$', 'events.views.members', name='event_members'),
)
