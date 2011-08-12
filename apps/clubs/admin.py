# -*- coding: utf-8 -*-
from clubs.models import Club
from clubs.models import Members

from django.contrib import admin

class ClubAdmin(admin.ModelAdmin):
    list_display        = ('title', 'admin', 'address')
    list_filter         = ('title', 'admin', 'address')
    search_fields       = ('title', 'admin', 'address')
    
class MembersAdmin(admin.ModelAdmin):
     list_display        = ('user', 'approved')

admin.site.register(Club, ClubAdmin)
admin.site.register(Members, MembersAdmin)
