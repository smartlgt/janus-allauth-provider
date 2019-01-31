from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model


class Adapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        try:
            user = get_user_model().objects.get(username=sociallogin.account.uid)
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)

            self._map_extra_data(user, sociallogin.account.extra_data)

        except get_user_model().DoesNotExist:
            pass

    def _map_extra_data(self, user, extra_data):
        # populate the extra data to the user on every login,
        # DO IT HERE, populate_user has only a fake user object

        user.is_superuser = extra_data.get('is_superuser', False)

        user.save()
