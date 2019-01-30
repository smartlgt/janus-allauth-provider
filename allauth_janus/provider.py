from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class JanusAccount(ProviderAccount):
    def to_str(self):
        return self.account.extra_data.get('name',
                                           super(JanusAccount, self).to_str())


class JanusProvider(OAuth2Provider):
    id = 'janus'
    name = 'Janus'
    account_class = JanusAccount

    def get_default_scope(self):
        return ['read']

    def extract_uid(self, data):
        return data['user_id']

    def extract_email_addresses(self, data):
        return [EmailAddress(email=data['email'],
                      verified=True,
                      primary=True)]

    def extract_common_fields(self, data):
        return dict(email=data['email'],
                    last_name=data['last_name'],
                    first_name=data['first_name'],
                    username=data['username'])


provider_classes = [JanusProvider]