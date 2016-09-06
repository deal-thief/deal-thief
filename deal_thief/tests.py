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


def test_register_view(dummy_request):
    """Test register_view."""
    from .views.default import register_view
    info = register_view(dummy_request)
    assert dummy_request.response.status_code == 200
    assert info['page_title'] == 'Register'
    assert info['error'] == ''


def test_check_credentials(dummy_request):
    """Test check_credentials function"""
    from .security import check_credentials
    pass

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


def test_layout_root_login(testapp):
    """Test layout root of home route."""
    response = testapp.get('/login', status=200)
    assert response.html.find('title').get_text() == "Deal Thief | Login"


def test_layout_root_register(testapp):
    """Test layout root of home route."""
    response = testapp.get('/register', status=200)
    assert response.html.find('title').get_text() == "Deal Thief | Register"


def test_layout_root_404(testapp):
    """Test layout root of 404 route."""
    response = testapp.get('/notfound', status=404)
    assert response.html.find('p').get_text() == "404 Page Not Found"


# ------- Mike's Functional Tests -------

def test_build_url(dummy_request):
    """Test the build url works from user input."""
    from .views.default import search_view
    my_params = {'location': 'seattle', 'start': '10/22/2016', 'end': '10/24/2016'}
    dummy_request.params.update(my_params)
    assert dummy_request.params['location'] == 'seattle'


def test_create_url_for_api_location_id():
    """Test that we can make an GET call to our API."""
    from .tools import create_url_for_api_location_id
    key = os.environ.get('SKYSCANNER_API_KEY')
    result = 'http://partners.api.skyscanner.net/apiservices/hotels/autosuggest/v2/US/USD/en-US/seattle?apikey=' + key
    assert create_url_for_api_location_id('seattle') == result
