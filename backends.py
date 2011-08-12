from django.contrib.auth.backends import ModelBackend
from django.contrib.admin.models import User
from profiles.models import Profile

class EmailAuthBackEnd(ModelBackend):
    def authenticate(self, email=None, password=None,**kwargs):
        try:
            user = User.objects.get(email=email)  

            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

class VkAuthBackEnd(ModelBackend):
    def authenticate(self, vk_id=None,**kwargs):
        try:
            profile = Profile.objects.get(vk_id=vk_id)  
            user = profile.user
            return user
        except:
            return None
