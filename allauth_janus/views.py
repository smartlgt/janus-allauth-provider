import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from django.conf import settings

from .provider import JanusProvider


class JanusOAuth2Adapter(OAuth2Adapter):
    provider_id = JanusProvider.id
    access_token_url = settings.ALLAUTH_JANUS_URL + '/o/token/'
    authorize_url = settings.ALLAUTH_JANUS_URL + '/o/authorize/'
    profile_url = settings.ALLAUTH_JANUS_URL + '/o/profile/'
    supports_state = True
    redirect_uri_protocol = settings.ALLAUTH_JANUS_REDIRECT_PROTOCOL

    def complete_login(self, request, app, token, **kwargs):
        response = requests.get(
            self.profile_url,
            params={'access_token': token})
        extra_data = response.json()
        extra_data2 =  {}
        if extra_data:
            extra_data2 = {
                'user_id': extra_data['id'],
                'last_name': extra_data['last_name'],
                'first_name': extra_data['first_name'],
                'name': extra_data['name'],
                'email': extra_data['email'],
                'username': extra_data['id'],
            }
        return self.get_provider().sociallogin_from_response(
            request,
            extra_data2)


oauth2_login = OAuth2LoginView.adapter_view(JanusOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(JanusOAuth2Adapter)