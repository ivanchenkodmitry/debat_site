# -*- coding: utf-8 -*-
from clubs.models import Club
from clubs.models import University
from django.contrib import admin

class ClubAdmin(admin.ModelAdmin):
    list_display        = ('title', 'admin', 'address')
    list_filter         = ('title', 'admin', 'address')
    search_fields       = ('title', 'admin', 'address')
    
class UniversityAdmin(admin.ModelAdmin):
  list_display        = ('title', 'address')

admin.site.register(Club, ClubAdmin)
admin.site.register(University, UniversityAdmin)
