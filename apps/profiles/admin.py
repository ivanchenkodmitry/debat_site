from django.contrib import admin
from profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'surname', 'club')
    list_filter         = ('user', 'surname', 'education', 'club')
admin.site.register(Profile, ProfileAdmin)
