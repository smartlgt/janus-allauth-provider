from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_updated

from allauth_janus.helper import janus_sync_user_properties

@receiver(social_account_updated)
def social_account_updated(sender, request, sociallogin, **kwargs):

    if sociallogin.account.provider == "janus":
        janus_sync_user_properties(request, sociallogin)

@receiver(user_signed_up)
def user_signed_up(sender, request, user, **kwargs):

    sociallogin = kwargs.get('sociallogin', None)

    if sociallogin and sociallogin.account.provider == "janus":
        janus_sync_user_properties(request, sociallogin)


