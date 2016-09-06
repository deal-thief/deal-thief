import os
from passlib.apps import custom_app_context as pwd_context
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated, Everyone

def includeme(config):
    """Security configuration"""
    auth_secret = os.environ.get('AUTH_SECRET', 'dealthiefsecret') 
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('public')
    config.set_root_factory(AppRoot)


class AppRoot(object):
    """Set up ACL"""
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'public'),
        (Allow, Authenticated, 'private')
    ]


def check_credentials(email, password, stored_user):
    """Verify email and password."""
    is_authenticated = False
    if email == stored_user.email:
        try:
            is_authenticated = pwd_context.verify(
                password, stored_user.password
            )
        except ValueError:
            pass
    return is_authenticated
