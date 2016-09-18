"""Security configuration for the app."""
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated, Everyone
from pyramid.session import SignedCookieSessionFactory


def includeme(config):
    """Security configuration."""
    session_secret = os.environ.get('SESSION_SECRET', 'itsaseekrit')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
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
