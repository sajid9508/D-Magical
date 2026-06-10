from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        try:
            # Check if input is an email address
            if '@' in username:
                user = UserModel.objects.get(email__iexact=username)
            else:
                # Treat username as phone number, match against UserProfile.phone_number
                user = UserModel.objects.get(profile__phone_number=username)
        except UserModel.DoesNotExist:
            # Fallback to standard username match
            try:
                user = UserModel.objects.get(username__iexact=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
