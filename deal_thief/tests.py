import pytest
import os
import transaction

from pyramid import testing


def test_home_view(dummy_request):
    """Test home template is in home view."""
    from .views.default import home_view
    info = home_view(dummy_request)
    assert info["page_title"] == 'Home'


def test_login_view(dummy_request):
    """Test template is in login view."""
    from .views.default import login_view
    info = login_view(dummy_request)
    assert info["page_title"] == 'Login'


def test_bad_route_404(dummy_request):
    """Test bad route returns 404."""
    from .views.notfound import notfound_view
    info = notfound_view(dummy_request)
    assert dummy_request.response.status_code == 404

# ---------Functional Tests-------------

def test_layout_root_home(testapp):
    """Test layout root of home route."""
    response = testapp.get('/', status=200)
    assert response.html.find('title').get_text() == "Deal Thief | Home"


def test_layout_root_404(testapp):
    """Test layout root of 404 route."""
    response = testapp.get('/notfound', status=404)
    assert response.html.find('p').get_text() == "404 Page Not Found"
