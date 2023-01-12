# installation

`pip install git+https://github.com/smartlgt/janus-allauth-provider@1.2.1#egg=allauth_janus`

# configuration
setup your `settings.py`:

```
INSTALLED_APPS = [
    # your setup with allauth and allauth.socialaccount
    'django.contrib.sites',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth_janus',
    
]
```


```
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# ALLAUTH settings
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True

# disable signup for all normal requests (allow them for your social providers)
ACCOUNT_ADAPTER = 'allauth_janus.adapter.NoNewUsersAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'allauth_janus.adapter.AllowNewUsersSocialAccountAdapter'

# path to redirect after login
LOGIN_REDIRECT_URL = "/"
# force sso login via the janus provider (don't display a login page on this website)
LOGIN_URL = "/accounts/janus/login/"

########################################
## JANUS
########################################
# define a custom function to handle your app need for data syncing
#ALLAUTH_JANUS_PRE_SOCIAL_CALLBACK = 'allauth_janus.helper.janus_sync_user_properties'  # (default)
ALLAUTH_JANUS_URL = 'https://sso.example.com/oauth2'
ALLAUTH_JANUS_REDIRECT_PROTOCOL = 'http'
ALLAUTH_JANUS_REMOTE_LOGOUT = True

# disable default linking by username on signup behavior (if account already exists)
# ALLAUTH_JANUS_PRE_SOCIAL_CALLBACK=allauth_janus.signals.noop  

SITE_ID = 1

```
## OIDC
```
# Enable usage of OIDC endpoints to retrieve userinfo
ALLAUTH_JANUS_OIDC = True 
# The preferred way to configure allauth providers.
SOCIALACCOUNT_PROVIDERS = {
    "janus": {
        # The client id and client secret can be configured via the admin backend (see #first run).
        # Alternatively they can be configured.
        "APP": {
            "client_id": "123",
            "secret": "456",
        },
        # Scope and PKCE can only be configured with this setting.
        # Default: `openid`
        "SCOPE": [
            "openid",
            "profile",
            "email"
        ],
        # Default: True
        "OAUTH_PKCE_ENABLED": True
    }
}
```

setup your man urls.py` and include allauth urls
```
path('accounts/', include('allauth.urls')),
```
the provider will automatically registered by allauth and a login/callback endpoint will be present at
`/accounts/janus/login/` and `/accounts/janus/login/callback/`


# first run

setup the social app credentials for the social app "janus"
`/admin/socialaccount/socialapp/add/`


# debug
if you see some `Social Network Login Failure` a good start is the OAuth2CallbackView class dispatch function

# sync custom data from janus
add your custom code to the signal handler for `social_account_updated` and `user_signed_up`

see `signals.py` for example

## sessions
your django sessions need to work, before a client leave the application and calls the sso, a random verifier and your login state will be stored in a session, on return this information need to be present.

### important session behavior
ensure your site framework ist configured correctly.

also if you debug/develop locally, use `localhost` instead of an ip. on ips your cookies may be disappearing.
