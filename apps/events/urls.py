from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # all ivent or latest photos
    url(r'^$', 'events.views.events', name="events"),
    # upload photos
    url(r'^add_event/$', 'events.views.add_event'),
    url(r'^add_event/latest/$', 'events.views.events', name='events'),
)
