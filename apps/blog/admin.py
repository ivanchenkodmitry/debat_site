# -*- coding: utf-8 -*-
from blog.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'publish', 'status2')
    list_filter         = ('publish', 'status')
    search_fields       = ('title', 'body', 'tease')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)