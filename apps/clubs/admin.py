# -*- coding: utf-8 -*-
from clubs.models import Club, Verification

from django.contrib import admin

class ClubAdmin(admin.ModelAdmin):
    list_display        = ('title', 'admin', 'address')
    list_filter         = ('title', 'admin', 'address')
    search_fields       = ('title', 'admin', 'address')
    
class VerificationAdmin(admin.ModelAdmin):
    list_display        = ('member', 'is_approved', 'club')
    list_filter         = ('is_approved', 'member', 'club')
    search_fields       = ('is_approved', 'member', 'club')

admin.site.register(Club, ClubAdmin)
admin.site.register(Verification, VerificationAdmin)
