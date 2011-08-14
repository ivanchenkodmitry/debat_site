from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Permission
from profiles.models import Profile

class EmailVkAuthBackEnd(ModelBackend):
	
	supports_object_permissions = False
	supports_anonymous_user = True
	supports_inactive_user = True
	
	def authenticate(self, email=None, password=None, vk_id=None, **kwargs):
		if vk_id:
			try:
				profile = Profile.objects.get(vk_id=vk_id)  
				user = profile.user
				return user
			except:
				return None
		elif email:
			try:
				user = User.objects.get(email=email)  
				if user.check_password(password):
					return user
			except User.DoesNotExist:
				return None
		return None

