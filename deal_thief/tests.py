import pytest
import os
import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from passlib.apps import custom_app_context as pwd_context
from .models import User, Search


def test_home_view(dummy_request):
    """Test home template is in home view."""
    from .views.default import home_view
    info = home_view(dummy_request)
    assert info["page_title"] == 'Home'

def test_home_view(dummy_request):
    """Test about_view."""
    from .views.default import about_view
    response = about_view(dummy_request)
    assert response["page_title"] == 'About'


def test_login_view(dummy_request):
    """Test template is in login view."""
    from .views.default import login_view
    info = login_view(dummy_request)
    assert dummy_request.response.status_code == 200
    assert info["page_title"] == 'Login'
    assert info['error'] == ''


def test_login_view_authenticated(mock_request):
    """login_view should redirect to home when user is authenticated."""
    from .views.default import login_view
    mock_request.authenticated_userid = 'test@user.com'
    response = login_view(mock_request)
    assert isinstance(response, HTTPFound)
    assert response.location == '/home'


def test_login_view_fail(mock_request):
    """login_view fail when incorrect credentials are provided."""
    from .views.default import login_view
    mock_request.params['email'] = 'incorrectemail'
    mock_request.params['password'] = 'incorrectpw'
    response = login_view(mock_request)
    assert response['error'] == 'Unsuccessful, try again'


def test_login_view_post_success(mock_request):
    """Test login_view when received a post method."""
    from .views.default import login_view
    mock_request.dbsession.add(User(
                email='test@user.com',
                password=pwd_context.encrypt('testpassword'),
                first_name='Test',
                last_name='User',
                city='City',
                state='WA'
    ))
    mock_request.params['email'] = 'test@user.com'
    mock_request.params['password'] = 'testpassword'
    response = login_view(mock_request)
    assert isinstance(response, HTTPFound)
    assert response.location == '/home'


def test_register_view(dummy_request):
    """Test register_view."""
    from .views.default import register_view
    info = register_view(dummy_request)
    assert dummy_request.response.status_code == 200
    assert info['page_title'] == 'Register'
    assert info['error'] == ''


def test_register_view_post_empty_field(mock_request):
    """Test register_view posted with empty form."""
    from .views.default import register_view
    response = register_view(mock_request)
    assert response['page_title'] == 'Register'
    assert response['error'] == 'All fields are required'


def test_register_view_post(mock_request):
    """Test register_view when received a post method."""
    from .views.default import register_view
    mock_request.params['first-name'] = 'Test'
    mock_request.params['last-name'] = 'User'
    mock_request.params['email'] = 'test@user.com'
    mock_request.params['password'] = 'testpassword'
    mock_request.params['confirm-password'] = 'testpassword'
    mock_request.params['city'] = 'City'
    mock_request.params['state'] = 'WA'
    response = register_view(mock_request)
    assert isinstance(response, HTTPFound)
    assert response.location == '/home'


def test_register_view_post_pw_not_matched(mock_request):
    """Test register_view when password does not match."""
    from .views.default import register_view
    mock_request.params['first-name'] = 'Test'
    mock_request.params['last-name'] = 'User'
    mock_request.params['email'] = 'test@user.com'
    mock_request.params['password'] = 'testpassword'
    mock_request.params['confirm-password'] = 'different'
    mock_request.params['city'] = 'City'
    mock_request.params['state'] = 'WA'
    response = register_view(mock_request)
    assert response['page_title'] == 'Register'
    assert response['error'] == 'Password didn\'t match'


def test_register_view_post_email_exists(mock_request):
    """Test register_view when it is posted an email already existed."""
    from .views.default import register_view
    mock_request.params['first-name'] = 'Test'
    mock_request.params['last-name'] = 'User'
    mock_request.params['email'] = 'test@user.com'
    mock_request.params['password'] = 'testpassword'
    mock_request.params['confirm-password'] = 'testpassword'
    mock_request.params['city'] = 'City'
    mock_request.params['state'] = 'WA'
    mock_request.dbsession.add(User(
                email='test@user.com',
                password=pwd_context.encrypt('testpassword'),
                first_name='Test',
                last_name='User',
                city='City',
                state='WA'
    ))
    response = register_view(mock_request)
    assert response['error'] == 'Email existed'


def test_register_view_authenticated(mock_request):
    """register_view should redirect to home when user is authenticated."""
    from .views.default import register_view
    mock_request.authenticated_userid = 'test@user.com'
    response = register_view(mock_request)
    assert isinstance(response, HTTPFound)
    assert response.location == '/home'


def test_verify_correct_credentials(test_user):
    """Test verify_credential method with correct credentials."""
    assert test_user.verify_credential('test@user.com', 'testpassword')


def test_verify_incorrect_credentials(test_user):
    """Test verify_credential method with incorrect credentials."""
    assert not test_user.verify_credential('test@user.com', 'randompw')


def test_verify_credentials_invalid_hash(test_user):
    """Test verify_credential method when stored pw is not hashed."""
    test_user.password = 'somethingnothashed'
    assert not test_user.verify_credential('test@user.com', 'randompw')


def test_logout_view(mock_request):
    """Test logout_view, make sure it return a HTTPFound obj."""
    from .views.default import logout_view
    response = logout_view(mock_request)
    assert isinstance(response, HTTPFound)


def test_dashboard_view(dummy_request):
    """Test dashboard_view."""
    from .views.default import dashboard_view
    response = dashboard_view(dummy_request)
    assert response['page_title'] == 'Dashboard'
    assert dummy_request.response.status_code == 200


def test_profile_view(dummy_request):
    """Test register_view."""
    from .views.default import profile_view
    response = profile_view(dummy_request)
    assert dummy_request.response.status_code == 200
    assert response['page_title'] == 'My profile'


def test_forbidden_view(mock_request):
    """Test forbidden_view, make sure it return a HTTPFound obj."""
    from .views.notfound import forbidden_view
    response = forbidden_view(mock_request)
    assert isinstance(response, HTTPFound)


def test_bad_route_404(dummy_request):
    """Test bad route returns 404."""
    from .views.notfound import notfound_view
    notfound_view(dummy_request)
    assert dummy_request.response.status_code == 404


# ---------Functional Tests-------------


def test_layout_root_home(testapp):
    """Test layout root of home route."""
    response = testapp.get('/')
    assert response.status_code == 200
    assert response.html.find('title').get_text() == "Deal Thief | Home"


def test_layout_root_login(testapp):
    """Test layout root of home route."""
    response = testapp.get('/login')
    assert response.status_code == 200
    assert response.html.find('title').get_text() == "Deal Thief | Login"


def test_layout_root_register_get(testapp):
    """Test layout root of home route."""
    response = testapp.get('/register')
    assert response.status_code == 200
    assert response.html.find('title').get_text() == "Deal Thief | Register"


def test_layout_root_dashboard_not_logged_in(testapp):
    """Test layout root of home route."""
    response = testapp.get('/dashboard', status='3*')
    assert response.status_code == 302


def test_layout_root_404(testapp):
    """Test layout root of 404 route."""
    response = testapp.get('/notfound', status='4*')
    assert response.status_code == 404
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


def test_create_url_for_hotel_list():
    """Test for getting hotel list."""
    from .tools import create_url_for_hotel_list
    key = os.environ.get('SKYSCANNER_API_KEY')
    location_id = '27547145'
    check_in = '12/04/2016'
    check_out = '12/10/2016'
    result = 'http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/US/USD/en-US/27547145/2016-12-04/2016-12-10/2/1?apiKey=' + key
    assert create_url_for_hotel_list(location_id, check_in, check_out) == result


def test_create_url_for_hotel_details():
    """Test we get hotel details."""
    from .tools import create_url_for_hotel_details
    session_location_header = '/apiservices/hotels/liveprices/v2/{{sessionkey}}?apikey={{encryptedkey}}'
    result = 'http://partners.api.skyscanner.net' + session_location_header
    assert create_url_for_hotel_details(session_location_header) == result


def test_create_url_hotel_id_list():
    """Test we create hotel id list."""
    from .tools import create_url_hotel_id_list
    hotel_id_list = [{'agent_prices': [{'id': 1, 'price_total': 102}], 'id': 47173467},
     {'agent_prices': [{'id': 124, 'price_total': 367}], 'id': 46948847},
     {'agent_prices': [{'id': 47, 'price_total': 182}], 'id': 46941437}]
    assert create_url_hotel_id_list(hotel_id_list) == '47173467,46948847,46941437'


def test_create_deep_link_url():
    """Test we make url for final get request."""
    from .tools import create_deep_link_url
    session_location_header = '/apiservices/hotels/livedetails/v2/details/{{sessionkey}}?apikey={{encryptedkey}}'
    hotel_ids = '[47173467, 46948847, 46941437, 134640597, 82030446, 46946183, 46944732, 114724112, 46943171, 105973506]'
    result = 'http://partners.api.skyscanner.net' + session_location_header + '&hotelIds=' + hotel_ids
    assert create_deep_link_url(hotel_ids, session_location_header) == result


def test_create_parsed_hotel_info():
    """Test we build an usable dictionary."""
    from .tools import create_parsed_hotel_info
    hotels = {"hotels_prices": [
        {"id": 1, "agent_prices": [{"price_per_room_night": 100,
                                    "price_total": 400,
                                    "booking_deeplink": "this is the deeplink"}]},
        {"id": 2, "agent_prices": [{"price_per_room_night": 150,
                                    "price_total": 5000,
                                    "booking_deeplink": "this is the deeplink2"}]}
                                ],
                "hotels": [
                {
                  "name": "Chicago Gateway Hostel",
                  "description": "Just a hostel",
                  "address": "hostile road",
                  "latitude": 41.9268,
                  "longitude": -87.64458,
                  "star_rating": 0
                },
                        {
                  "name": "Chicago Gateway Hostel",
                  "description": "Just a hostel",
                  "address": "hostile road",
                  "latitude": 41.9268,
                  "longitude": -87.64458,
                  "star_rating": 0
                        }],
              }
    assert len(create_parsed_hotel_info(hotels)) == 2
