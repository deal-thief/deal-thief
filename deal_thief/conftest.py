"""Conftest file the does the prep work prior tests run."""
import pytest
from passlib.apps import custom_app_context as pwd_context
from pyramid import testing
from .models import (
        User,
        Search,
        get_engine,
        get_session_factory,
        get_tm_session
)
from .models.meta import Base
import transaction


class MockRequest(object):
    """MockRequest intended to be a better version of testing.DummyRequest."""

    def __init__(self, **kwargs):
        """Init a MockRequest instance."""
        self.__dict__.update(kwargs)

    def route_url(self, string):
        """Mimic the pyramid.request.Request route_url."""
        return '/{}'.format(string)


class MockSession(object):
    def __init__(self, **kwargs):
        """Init a MockSession instance."""
        self.flash_msg = []
        self.__dict__.update(kwargs)

    def flash(self, string):
        """Mimic the pyramid.session.flash object."""
        self.flash_msg.append(string)


@pytest.fixture(scope='session')
def sqlengine(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include(".models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope='function')
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def dummy_request(new_session):
    """Call a dummy request."""
    test_request = testing.DummyRequest()
    test_request.dbsession = new_session
    return test_request


@pytest.fixture(scope='function')
def mock_request(new_session):
    """Fixture passing mock_request obj to tests."""
    return MockRequest(
            method='POST',
            authenticated_userid=None,
            dbsession=new_session,
            params={},
            session=MockSession()
    )


@pytest.fixture(scope='function')
def testapp():
    """Setup TestApp."""
    from deal_thief import main
    settings = {'sqlalchemy.url': 'sqlite:///:memory:'}
    app = main({}, **settings)
    from webtest import TestApp
    return TestApp(app)


@pytest.fixture(scope='function')
def test_user():
    """Create test_user object as an instance of User model."""
    test_user = User()
    test_user.email = 'test@user.com'
    test_user.password = pwd_context.encrypt('testpassword')
    return test_user
