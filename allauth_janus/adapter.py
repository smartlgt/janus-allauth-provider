from django.contrib.auth.models import User

from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class Adapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        try:
            user = User.objects.get(username=sociallogin.account.uid)
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass
