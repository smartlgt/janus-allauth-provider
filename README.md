# installation

ToDo:
`pip install`

# configuration
setup your `settings.py`:

```
INSTALLED_APPS = [
    # your setup with allauth and allauth.socialaccount
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'janus_provider',
    
]
```


```
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# ALLAUTh settigs
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True

SOCIALACCOUNT_ADAPTER = 'allauth_janus.adapter.Adapter'

LOGIN_REDIRECT_URL = "/"

########################################
## JANUS
########################################
ALLAUTH_JANUS_URL = 'https://janus.example.com'
ALLAUTH_JANUS_REDIRECT_PROTOCOL = 'http'

SITE_ID = 1

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

## sessions
your django sessions need to work, before a client leave the application and calls the sso, a random verifier and your login state will be stored in a session, on return this information need to be present.

### important session behavior
ensure your site framework ist configured correctly.

also if you debug/develop locally, use `localhost` instead of an ip. on ips your cookies may be disappearing.