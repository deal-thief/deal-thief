import pytest
from passlib.apps import custom_app_context as pwd_context
from pyramid import testing


@pytest.fixture(scope="function")
def dummy_request():
    """Call a dummy request."""
    return testing.DummyRequest()


@pytest.fixture(scope="function")
def testapp():
    """Setup TestApp."""
    from deal_thief import main
    app = main({})
    from webtest import TestApp
    return TestApp(app)


@pytest.fixture(scope="function")
def test_user():
    from .models import User
    test_user = User()
    test_user.email = 'test@user.com'
    test_user.password = pwd_context.encrypt('testpassword')
    return test_user
