from django.conf.urls.defaults import *

urlpatterns = patterns('',


    # all ivent or latest ivent
    url(r'^$', 'events.views.events', name="events"),
    # Add event
    url(r'^add_event/$', 'events.views.add_event', name="add_event"),
    # an event details
    url(r'^details/(?P<id>\d+)/$', 'events.views.details', name="events_details"),
    url(r'^destroy/(?P<id>\d+)/$', 'events.views.destroy', name='events_destroy'),
)
