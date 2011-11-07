# -*- coding: utf-8 -*-
from events.models import Event, AnswerList

from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    list_display        = ('title', 'date_begin', 'date_end', 'address', 'creator', 'approved')
    list_filter         = ('approved',)
    search_fields       = ('title', 'address', 'description')

admin.site.register(Event, EventAdmin)
admin.site.register(AnswerList)


