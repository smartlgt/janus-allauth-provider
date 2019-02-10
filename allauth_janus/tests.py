"""Test Janus OAuth2"""
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import JanusProvider


class JanusTests(OAuth2TestsMixin, TestCase):

    provider_id = JanusProvider.id

    def get_mocked_response(self):
        """Test authentication with an non-null avatar."""
        return MockedResponse(200, """{
            "id": "adminusername",
            "first_name": "Marie Jayen",
            "last_name": "Do",
            "name": "Marie Jayen Do",
            "email": "test@eyample.com",
            "email_verified": true,
            "is_superuser": true,
            "can_authenticate": true,
            "groups": ["admin", "staff"]
        }""")