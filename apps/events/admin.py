# -*- coding: utf-8 -*-
from events.models import Event, Member

from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    list_display        = ('title', 'date', 'address', 'creator', 'approved')
    list_filter         = ('approved',)
    search_fields       = ('title', 'address', 'description')

admin.site.register(Event, EventAdmin)
admin.site.register(Member)


