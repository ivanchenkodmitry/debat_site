# -*- coding: utf-8 -*-
from universities.models import University
from django.contrib import admin

class UniversityAdmin(admin.ModelAdmin):
  list_display        = ('title', 'address')
  
  
admin.site.register(University, UniversityAdmin)