import pytest

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
