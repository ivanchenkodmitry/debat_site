
from django.contrib import admin
from photofiler.models import Photo

class PhotoAdmin(admin.ModelAdmin):

    list_display = ['get_thumbnail_html', 'title']
    list_display_links = ['get_thumbnail_html']
        
admin.site.register(Photo, PhotoAdmin)
