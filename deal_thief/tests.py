import pytest
import os
import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from passlib.apps import custom_app_context as pwd_context
from requests import Response
from .models import User, Search
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock
import json


def test_home_view(dummy_request):
    """Test home template is in home view."""
    from .views.default import home_view
    info = home_view(dummy_request)
    assert info["page_title"] == 'Home'


def test_about_view(dummy_request):
    """Test home template is in home view."""
    from .views.default import home_view
    info = home_view(dummy_request)
    assert info["page_title"] == 'Home'


def test_login_view(dummy_request):
    """Test about view."""
    from .views.default import about_view
    response = about_view(dummy_request)
    assert dummy_request.response.status_code == 200
    assert response["page_title"] == 'About'


def test_login_view_authenticated(mock_request):
    """login_view should redirect to home when user is authenticated."""
    from .views.default import login_view
    mock_request.authenticated_userid = 'test@user.com'
    response = login_view(mock_request)
    assert isinstance(response, HTTPFound)
    assert response.location == '/home'


def test_login_view_fail(mock_request):
    """login_view should fail when incorrect credentials are provided."""
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


def test_register_view_post_empty_field(mock_request):
    """Test register_view posted with empty form."""
    from .views.default import register_view
    response = register_view(mock_request)
    assert isinstance(response, HTTPFound)
    assert response.location == '/login'


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
    assert isinstance(response, HTTPFound)
    assert response.location == '/login'


def test_register_view_post_pw_not_matched(mock_request):
    """Test register_view when it is posted an email already existed."""
    from .views.default import register_view
    mock_request.params['first-name'] = 'Test'
    mock_request.params['last-name'] = 'User'
    mock_request.params['email'] = 'test@user.com'
    mock_request.params['password'] = 'testpassword'
    mock_request.params['confirm-password'] = 'something'
    mock_request.params['city'] = 'City'
    mock_request.params['state'] = 'WA'
    response = register_view(mock_request)
    assert isinstance(response, HTTPFound)
    assert response.location == '/login'


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


def test_dashboard_view(mock_request):
    """Test dashboard_view."""
    from .views.default import dashboard_view
    mock_request.dbsession.add(User(
                email='test@user.com',
                password=pwd_context.encrypt('testpassword'),
                first_name='Test',
                last_name='User',
                city='City',
                state='WA'
    ))
    mock_request.authenticated_userid = 'test@user.com'
    response = dashboard_view(mock_request)
    assert response['page_title'] == 'Dashboard'


def test_profile_view_get(mock_request):
    """Test get profile_view."""
    from .views.default import profile_view
    mock_request.dbsession.add(User(
                email='test@user.com',
                password=pwd_context.encrypt('testpassword'),
                first_name='Test',
                last_name='User',
                city='City',
                state='WA'
    ))
    mock_request.authenticated_userid = 'test@user.com'
    mock_request.method = 'GET'
    response = profile_view(mock_request)
    assert response['page_title'] == 'My profile'
    assert response['user'].email == 'test@user.com'


def test_profile_view_post_success(mock_request):
    """Test post profile_view."""
    from .views.default import profile_view
    mock_request.dbsession.add(User(
                email='test@user.com',
                password=pwd_context.encrypt('testpassword'),
                first_name='Test',
                last_name='User',
                city='City',
                state='WA'
    ))
    mock_request.authenticated_userid = 'test@user.com'
    mock_request.params['current-password'] = 'testpassword'
    mock_request.params['new-password'] = 'newpw'
    mock_request.params['confirm-new-password'] = 'newpw'
    response = profile_view(mock_request)
    assert response['page_title'] == 'My profile'
    assert response['user'].email == 'test@user.com'
    assert response['message']['type'] == 'success'
    assert response['message']['detail'] == 'Password updated'


def test_profile_view_post_unmatched_new_pw(mock_request):
    """Test post profile_view."""
    from .views.default import profile_view
    mock_request.dbsession.add(User(
                email='test@user.com',
                password=pwd_context.encrypt('testpassword'),
                first_name='Test',
                last_name='User',
                city='City',
                state='WA'
    ))
    mock_request.authenticated_userid = 'test@user.com'
    mock_request.params['current-password'] = 'testpassword'
    mock_request.params['new-password'] = 'newpw'
    mock_request.params['confirm-new-password'] = 'newpw123'
    response = profile_view(mock_request)
    assert response['page_title'] == 'My profile'
    assert response['user'].email == 'test@user.com'
    assert response['message']['type'] == 'error'
    assert response['message']['detail'] == 'New passwords did not match'


def test_profile_view_post_wrong_current_pw(mock_request):
    """Test post profile_view."""
    from .views.default import profile_view
    mock_request.dbsession.add(User(
                email='test@user.com',
                password=pwd_context.encrypt('testpassword'),
                first_name='Test',
                last_name='User',
                city='City',
                state='WA'
    ))
    mock_request.authenticated_userid = 'test@user.com'
    mock_request.params['current-password'] = 'wrongpassword'
    mock_request.params['new-password'] = 'newpw'
    mock_request.params['confirm-new-password'] = 'newpw'
    response = profile_view(mock_request)
    assert response['page_title'] == 'My profile'
    assert response['user'].email == 'test@user.com'
    assert response['message']['type'] == 'error'
    assert response['message']['detail'] == 'Incorrect current password'


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
    """Regiter view get should return 404 because it only allow post."""
    response = testapp.get('/register', status='4*')
    assert response.status_code == 404


def test_layout_root_dashboard_not_logged_in(testapp):
    """Test layout root of home route."""
    response = testapp.get('/dashboard', status='3*')
    assert response.status_code == 302


def test_layout_root_404(testapp):
    """Test layout root of 404 route."""
    response = testapp.get('/notfound', status='4*')
    assert response.status_code == 404
    assert response.html.find('h4').get_text() == "404 Page Not Found"


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
    hotel_id_list = [
        {'agent_prices': [{'id': 1, 'price_total': 102}], 'id': 47173467},
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

NEW_JSON = {"places": [
    {
      "place_id": 1,
      "city_name": "Seattle",
      "admin_level1": "WA",
      "country_name": "United States",
      "admin_level2": "King"
    },
    {
      "place_id": 2,
      "city_name": "Seattle Heights",
      "admin_level1": "WA",
      "country_name": "United States",
      "admin_level2": "Snohomish"
    }],
    "results": [
    {
      "display_name": "Seattle",
      "parent_place_id": 1,
      "individual_id": "27538444",
      "geo_type": "City",
      "localised_geo_type": "City",
      "is_bookable": 'false'
    },
    {
      "display_name": "Seattle / Tacoma International (SEA)",
      "parent_place_id": 1,
      "individual_id": "95673694",
      "geo_type": "Airport",
      "localised_geo_type": "Airport",
      "is_bookable": 'false'
    }]}

HEADERS = {
    'Cahce-Control': 'no-cache',
    'Content-Encodng': 'gzip',
    'Content-Length': '4841',
    'Content-Type': 'text/javascript;charset=utf-8',
    'Date': 'Thu, 08 Sep 2015 21:11:42 GMT',
    'Expires': '1',
    'Location': 'api/services/etc',
    'Vary': 'Accept-Encoding',
}

HOTEL_LIST = {'hotels_prices': [
    {'agent_prices': [{'id': 1, 'price_total': 130}], 'id': 136452598},
    {'agent_prices': [{'id': 129, 'price_total': 200}], 'id': 46946922},
    {'agent_prices': [{'id': 106, 'price_total': 247}], 'id': 46971209}]
}

HOTELS = {"hotels_prices": [
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

FINAL_INFO = [
    {
        'latitude': 41.9268,
        'address': 'hostile road',
        'star_rating': 0,
        'booking_deeplink':
        'this is the deeplink',
        'nightly_price': 100,
        'description': 'Just a hostel',
        'price_total': 400,
        'name': 'Chicago Gateway Hostel',
        'longitude': -87.64458,
        'id': 1
    },
    {
        'latitude': 41.9268,
        'address': 'hostile road',
        'star_rating': 0,
        'booking_deeplink': 'this is the deeplink2',
        'nightly_price': 150,
        'description': 'Just a hostel',
        'price_total': 5000,
        'name': 'Chicago Gateway Hostel',
        'longitude': -87.64458,
        'id': 2
    }]

ERROR = ''


@patch('requests.get')
def test_get_location_id(req):
    """Test getting of location id."""
    from .views.default import get_location_id
    mock_response = MagicMock(spec=Response, status_code=200, response=json.dumps(NEW_JSON))
    req.return_value = mock_response
    mock_response.json.return_value = NEW_JSON
    result = get_location_id('seattle')
    assert result == "27538444"


@patch('requests.get')
def test_get_session(req):
    """Test getting session info from API."""
    from .views.default import get_session
    mock_response = MagicMock(spec=Response, status_code=200, headers=HEADERS)
    req.return_value = mock_response
    result = get_session('2753844', '10/24/2016', '10/28/2016')
    assert result == 'api/services/etc'


@patch('requests.get')
def test_get_hotel_id_list(req):
    """Test get hotel ID list from API."""
    from .views.default import get_hotel_id_list
    mock_response = MagicMock(spec=Response, status_code=200, response=json.dumps(HOTEL_LIST))
    req.return_value = mock_response
    mock_response.json.return_value = HOTEL_LIST
    result = get_hotel_id_list('session')
    assert result == '136452598,46946922,46971209'


@patch('requests.get')
def test_get_hotel_info(req):
    """Test get hotel info and prices from API."""
    from .views.default import get_hotel_info
    mock_response = MagicMock(spec=Response, status_code=200, response=json.dumps(HOTELS))
    req.return_value = mock_response
    mock_response.json.return_value = HOTELS
    result = get_hotel_info('hotel_id_list', 'session')
    assert result == FINAL_INFO


@patch('deal_thief.views.default.get_hotel_info')
@patch('deal_thief.views.default.get_hotel_id_list')
@patch('deal_thief.views.default.get_session')
@patch('deal_thief.views.default.get_location_id')
def test_search_view(location_id, session, hotel_id_list, hotel_info):
    """Test search view returns correct final info."""
    from .views.default import search_view
    mock_request = testing.DummyRequest()
    mock_request.params['location'] = 'Seattle'
    mock_request.params['start'] = '10/14/2016'
    mock_request.params['end'] = '10/16/2016'
    location_id.return_value = '136452598'
    session.return_value = 'api/services/etc'
    hotel_id_list.return_value = '136452598,46946922,46971209'
    hotel_info.return_value = FINAL_INFO
    response = search_view(mock_request)
    assert response['hotel_info'] == FINAL_INFO
