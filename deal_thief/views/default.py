from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import requests
from passlib.apps import custom_app_context as pwd_context
from pyramid.security import remember, forget, authenticated_userid
from ..models import User, Search
from ..tools import (create_url_for_api_location_id, create_url_for_hotel_list,
                    create_url_for_hotel_details, create_url_hotel_id_list,
                    create_deep_link_url, create_parsed_hotel_info)


@view_config(route_name='home', renderer='../templates/home.html')
def home_view(request):
    return {
        'page_title': 'Home',
        'is_authenticated': authenticated_userid(request)
    }


@view_config(route_name='register', renderer='../templates/register.html')
def register_view(request):
    if authenticated_userid(request):
        return HTTPFound(location=request.route_url('home'))
    error = ''
    if request.method == 'POST':
        first_name = request.params.get('first-name', '')
        last_name = request.params.get('last-name', '')
        email = request.params.get('email', '')
        password = request.params.get('password', '')
        city = request.params.get('city', '')
        state = request.params.get('state', '')
        if first_name and last_name and email and password and city and state:
            if request.dbsession.query(User).\
                    filter_by(email=email).count() == 0:
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=pwd_context.encrypt(password),
                    city=city,
                    state=state
                )
                request.dbsession.add(new_user)
                headers = remember(request, email)
                return HTTPFound(
                        location=request.route_url('home'),
                        headers=headers
                )
            else:
                error = 'Email existed'
        else:
            error = 'All fields are required'
    return {
        'page_title': 'Register',
        'error': error
    }


@view_config(route_name='login', renderer='../templates/login.html')
def login_view(request):
    """View for login page."""
    if authenticated_userid(request):
        return HTTPFound(location=request.route_url('home'))
    error = ''
    if request.method == 'POST':
        email = request.params.get('email', '')
        password = request.params.get('password', '')
        if email and password:
            query = request.dbsession.query(User).filter_by(email=email)
            stored_user = query.first()
            if stored_user:
                if stored_user.verify_credential(email, password):
                    headers = remember(request, email)
                    return HTTPFound(
                            location=request.route_url('home'),
                            headers=headers
                    )
        error = 'Unsuccessful, try again'

    return {
        'page_title': 'Login',
        'error': error
    }


@view_config(route_name='logout')
def logout_view(request):
    """Clear cookie, log user out and redirect to home_view."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(
        route_name='dashboard',
        renderer='../templates/dashboard/saved_searches.html',
        permission='private'
)
def dashboard_view(request):
    """Dashboard view for user."""
    return {
        'page_title': 'Dashboard'
    }


@view_config(
        route_name='profile',
        renderer='../templates/dashboard/profile.html',
        permission='private'
)
def profile_view(request):
    """Profile view for user."""
    return {
        'page_title': 'My profile'
    }


def get_location_id(location):
    """Get location id from API based on user input."""
    location_id_url = create_url_for_api_location_id(location)
    import pdb; pdb.set_trace()
    location_id_unparsed = requests.get(location_id_url)
    location_id_unparsed.raise_for_status()
    location_id = location_id_unparsed.json()['results'][0]['individual_id']
    return location_id


def get_session(location_id, checkin, checkout):
    """Get session info from API."""
    session_start_url = create_url_for_hotel_list(location_id, checkin, checkout)
    session = requests.get(session_start_url, headers={'Content-Type': 'application/json'})
    return session.headers['Location']


def get_hotel_id_list(session):
    """Get hotel id list from API."""
    hotel_detail_url = create_url_for_hotel_details(session)
    hotel_detail_unparsed = requests.get(hotel_detail_url)
    hotel_id_list = hotel_detail_unparsed.json()['hotels_prices']
    new_hotel_list_id = create_url_hotel_id_list(hotel_id_list)
    return new_hotel_list_id


def get_hotel_info(hotel_id_list, session):
    """Get hotel info and prices from API."""
    final_url = create_deep_link_url(hotel_id_list, session)
    hotel_info_unparsed = requests.get(final_url)
    hotels = hotel_info_unparsed.json()
    final_info = create_parsed_hotel_info(hotels)
    return final_info


@view_config(route_name='search', renderer='../templates/search.html')
def search_view(request):
    """Give us our search view."""
    location = request.params['location']
    checkin = request.params['start']
    checkout = request.params['end']

    location_id = get_location_id(location)
    session = get_session(location_id, checkin, checkout)
    hotel_id_list = get_hotel_id_list(session)
    final_info = get_hotel_info(hotel_id_list, session)
    return {"hotel_info": final_info}


'''
request.session = {
    (location, checkin, checkout) : {
        'location_id': get_location_id(location),
        'session': get_session(location, checkin, checkout),
        'hotel_ids': get_hotel_ids(session),
        'last_updates': datetime
    }
}
'''
