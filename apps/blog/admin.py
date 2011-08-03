# -*- coding: utf-8 -*-
from blog.models import Post
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'publish', 'status2')
    list_filter         = ('publish', 'status')
    search_fields       = ('title', 'body', 'tease')
    prepopulated_fields = {'slug': ('title',)}
    
    def save(self, force_insert=False, force_update=False):
        self.updated_at = datetime.now()
        super(PostAdmin, self).save(force_insert, force_update)
        

admin.site.register(Post, PostAdmin)