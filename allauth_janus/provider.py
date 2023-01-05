from allauth_janus.app_settings import ALLAUTH_JANUS_CUSTOM_SCOPES, ALLAUTH_JANUS_OIDC

from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

from allauth_janus.helper import extract_username


class JanusAccount(ProviderAccount):
    def to_str(self):
        return self.account.extra_data.get('name',
                                           super(JanusAccount, self).to_str())


class JanusProvider(OAuth2Provider):
    id = 'janus'
    name = 'Janus'
    account_class = JanusAccount

    def get_default_scope(self):
        return ['openid']

    def get_scope(self, request):
        # Use custom scopes if set else use default.
        scope = ALLAUTH_JANUS_CUSTOM_SCOPES or self.get_default_scope()
        dynamic_scope = request.GET.get("scope", None)
        if dynamic_scope:
            scope.extend(dynamic_scope.split(","))
        return scope

    # The `uid` and `username` must be the same.
    # The actual user data is written to the User model in `map_extra_data`.
    def extract_uid(self, data):
        return extract_username(data, ALLAUTH_JANUS_OIDC)

    def extract_common_fields(self, data):
        return {'username': extract_username(data, ALLAUTH_JANUS_OIDC)}


provider_classes = [JanusProvider]
