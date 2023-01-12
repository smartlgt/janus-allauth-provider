from django.conf import settings

# False to not break existing deployments. Uses old custom endpoints when disabled.
ALLAUTH_JANUS_OIDC = getattr(settings, "ALLAUTH_JANUS_OIDC", False)

if ALLAUTH_JANUS_OIDC:
    ALLAUTH_JANUS_PROFILE_URL = settings.ALLAUTH_JANUS_URL + '/o/userinfo/'
else:
    ALLAUTH_JANUS_PROFILE_URL = settings.ALLAUTH_JANUS_URL + '/o/profile/'
