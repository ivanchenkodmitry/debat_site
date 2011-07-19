from django.conf.urls.defaults import *

urlpatterns = patterns('',


    # all ivent or latest ivent
    url(r'^$', 'events.views.events', name="events"),
    # Add event
    url(r'^add_event/$', 'events.views.add_event', name="add_event"),
    # an event details
    url(r'^details/(?P<id>\d+)/$', 'events.views.details', name="event_details"),
    url(r'^destroy/(?P<id>\d+)/$', 'events.views.destroy', name='event_destroy'),
    #edit event
    url(r'^edit/(?P<id>\d+)/$', 'events.views.edit', name='event_edit'),
)
