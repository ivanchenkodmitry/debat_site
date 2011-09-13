# -*- coding: utf-8 -*-
from projects.models import Project
from django.contrib import admin
from django.conf import settings
from django.db import models


class ProjectAdmin(admin.ModelAdmin):
    list_display        = ('title', 'author')
    
    #prepopulated_fields = {'slug': ('title',)}
    
    
admin.site.register(Project, ProjectAdmin)
