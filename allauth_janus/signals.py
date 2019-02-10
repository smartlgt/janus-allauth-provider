from allauth.socialaccount.signals import pre_social_login
from django.conf import settings
from django.dispatch import receiver
from django.utils.module_loading import import_string

from allauth_janus.helper import janus_sync_user_properties

def load_function(path):
    return import_string(path)

@receiver(pre_social_login)
def pre_social_login_handler(sender, request, sociallogin, **kwargs):

    if sociallogin.account.provider == "janus":

        if hasattr(settings, 'ALLAUTH_JANUS_PRE_SOCIAL_CALLBACK'):
            func = load_function(settings.ALLAUTH_JANUS_PRE_SOCIAL_CALLBACK)
            func(sender, request, sociallogin, **kwargs)
        else:
            # call default function
            janus_sync_user_properties(request, sociallogin)


