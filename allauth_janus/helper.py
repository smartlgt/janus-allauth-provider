from allauth_janus.app_settings import ALLAUTH_JANUS_OIDC, ALLAUTH_JANUS_CUSTOM_SCOPES
from django.contrib.auth import get_user_model

def janus_sync_user_properties(request, sociallogin):
    try:
        # force connecting of an existing user with the same username
        # if we remove this, a user that already exists in the local database and was not signed up via janus will
        # not be able to login and will hang
        user = get_user_model().objects.get(username=sociallogin.account.uid)
        if not sociallogin.is_existing:
            sociallogin.connect(request, user)

        map_extra_data(user, sociallogin.account.extra_data)

    except get_user_model().DoesNotExist:
        pass


def map_extra_data(user, extra_data):
    # populate the extra data to the user on every login,
    # DO IT HERE, populate_user has only a fake user object

    # permissions
    user.is_superuser = extra_data.get('is_superuser', False)
    user.is_staff = extra_data.get('is_staff', False)
    if user.is_superuser:
        user.is_staff = True  # also allow superuser to log into the admin panel

    groups = extra_data.get('groups', [])

    # do this more carefully, only remove user from group if not present anymore
    # not remove all and add them all again

    for gg in user.groups.all():
        if gg.name not in groups:
            user.groups.remove(gg)

    for group in groups:
        from django.contrib.auth.models import Group
        try:
            group_object = Group.objects.get(name=group)
            user.groups.add(group_object)
        except Group.DoesNotExist as e:
            # log this but don't raise an exception
            pass

    # user data
    if ALLAUTH_JANUS_OIDC:
        if 'preferred_username' in extra_data:
            user.username = extra_data.get('preferred_username', '')
        else:
            user.username = extra_data.get('sub', '')
        user.first_name = extra_data.get('given_name', '')
        user.last_name = extra_data.get('family_name', '')
    else:
        user.username = extra_data.get('id', '')
        user.first_name = extra_data.get('first_name', '')
        user.last_name = extra_data.get('last_name', '')

    # sync email via user allauth class
    email = extra_data.get('email', None)
    email_verified = extra_data.get('email_verified', False)

    from allauth.account.models import EmailAddress
    if email:
        # remove the old emails
        EmailAddress.objects.filter(user=user).exclude(email=email).delete()

        if EmailAddress.objects.filter(email=email).exists():
            em = EmailAddress.objects.filter(email=email).first()
            em.verified = email_verified
            em.save()
            em.set_as_primary()  # update user table email field
        else:
            em = EmailAddress.objects.create(user=user, email=email, verified=email_verified)
            em.set_as_primary()  # update user table email field
    else:

        # remove email from user field and delete the email address from allauth
        old_email = user.email
        if old_email:
            user.email = ""
            EmailAddress.objects.filter(user=user).delete()

    user.save()


def extract_username(data: dict, is_oidc: bool) -> str:
    if is_oidc and 'profile' in ALLAUTH_JANUS_CUSTOM_SCOPES:
        # If the `profile` scope is being requested the username should be available.
        return data['preferred_username']
    elif is_oidc:
        return data['sub']
    else:
        return data['id']
