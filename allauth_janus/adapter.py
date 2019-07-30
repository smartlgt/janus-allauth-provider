from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter


class Adapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # using the adapter pre_social_login function is is deprecated, use the signal
        pass




class AllowNewUsersSocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return True

class NoNewUsersAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return False