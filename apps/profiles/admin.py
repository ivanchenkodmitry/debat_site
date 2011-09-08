from django.contrib import admin
from profiles.models import Profile, Verification

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'surname')
    list_filter         = ('user', 'surname', 'education')

class VerificationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'md5_hash')
    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Verification, VerificationAdmin)
