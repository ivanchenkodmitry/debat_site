# -*- coding: utf-8 -*-
from blog.models import Post
from django.contrib import admin
from django.conf import settings
from django.db import models

if "notification" in settings.INSTALLED_APPS:
  from notification import models as notification
else:
    notification = None
try:
  from friends.models import Friendship
  friends = True
except ImportError:
    friends = False


class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'author', 'publish', 'status2')
    list_filter         = ('publish', 'status')
    search_fields       = ('title', 'body', 'tease')
    prepopulated_fields = {'slug': ('title',)}
    
    def save_model(self, request, obj, form, change):
      if notification:
        #  if post.status2==1:
                if friends:
                                notification.send((x['friend'] for x in Friendship.objects.friends_for_user(obj.author)), "blog_friend_post", {"post": obj})
      obj.save()  


admin.site.register(Post, PostAdmin)
