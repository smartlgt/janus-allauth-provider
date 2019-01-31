from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model


class Adapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        try:
            user = get_user_model().objects.get(username=sociallogin.account.uid)
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)
        except get_user_model().DoesNotExist:
            pass
