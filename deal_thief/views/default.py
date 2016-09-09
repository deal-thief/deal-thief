from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import requests
from passlib.apps import custom_app_context as pwd_context
from pyramid.security import remember, forget, authenticated_userid
from ..models import User, Search
from ..tools import (
        create_url_for_api_location_id,
        create_url_for_hotel_list,
        create_url_for_hotel_details,
        create_url_hotel_id_list,
        create_deep_link_url,
        create_parsed_hotel_info
)


@view_config(route_name='home', renderer='../templates/home.html')
def home_view(request):
    return {
        'page_title': 'Home',
        'is_authenticated': authenticated_userid(request)
    }


@view_config(route_name='register', request_method='POST')
def register_view(request):
    if authenticated_userid(request):
        return HTTPFound(location=request.route_url('home'))
    error = ''
    first_name = request.params.get('first-name', '')
    last_name = request.params.get('last-name', '')
    email = request.params.get('email', '')
    password = request.params.get('password', '')
    confirm_password = request.params.get('confirm-password', '')
    city = request.params.get('city', '')
    state = request.params.get('state', '')
    if first_name and last_name and email and password and city and state\
            and password == confirm_password:
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
    elif password != confirm_password:
        error = 'Password didn\'t match'
    else:
        error = 'All fields are required'
    request.session.flash(error)
    return HTTPFound(
        location=request.route_url('login'),
    )


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
        renderer='../templates/dashboard/dashboard.html',
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
    message = {}
    email = authenticated_userid(request)
    query = request.dbsession.query(User).filter_by(email=email)
    user = query.first()
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        current_password = request.params.get('current-password', '')
        if pwd_context.verify(current_password, user.password):
            new_password = request.params.get('new-password', '')
            confirm_new_password = request.params.get('confirm-new-password', '')
            if new_password and confirm_new_password and\
                    new_password == confirm_new_password:
                user.password = pwd_context.encrypt(new_password)
                request.dbsession.add(user)
                message['type'] = 'success'
                message['detail'] = 'Password updated'
            else:
                message['type'] = 'error'
                message['detail'] = 'New passwords did not match'
        else:
            message['type'] = 'error'
            message['detail'] = 'Incorrect current password'
    return {
        'page_title': 'My profile',
        'message': message,
        'user': user
    }


@view_config(route_name='about', renderer='../templates/about.html')
def about_view(request):
    """View for about page."""
    return {
        'page_title': 'About',
        'is_authenticated': authenticated_userid(request)
    }


def get_location_id(location):
    """Get location id from API based on user input."""
    location_id_url = create_url_for_api_location_id(location)
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
    max_retries = 5
    retry_count = 0
    final_info = []
    while retry_count < max_retries:
        try:
            final_url = create_deep_link_url(hotel_id_list, session)
            hotel_info_unparsed = requests.get(final_url)
            hotels = hotel_info_unparsed.json()
            final_info = create_parsed_hotel_info(hotels)
        except ValueError:
            retry_count += 1
            continue
        else:
            break
    return final_info


@view_config(route_name='search', renderer='../templates/search.html')
def search_view(request):
    """Give us our search view."""
    error = ''
    final_info = {}
    location = request.params.get('location', '')
    checkin = request.params.get('start', '')
    checkout = request.params.get('end', '')
    if location and checkin and checkout:


    # key = (location, checkin, checkout)
    # if key not in request.session:
    #     loc_id = get_location_id(location)
    #     api_session = get_session(location_id, checkin, checkout)
    #     request.session[key] = api_session
    # session = request.session[key]

        location_id = get_location_id(location)
        try:
            session = get_session(location_id, checkin, checkout)
            hotel_id_list = get_hotel_id_list(session)
            try:
                final_info = get_hotel_info(hotel_id_list, session)
            except KeyError:
                error = 'There is no hotel information available for this input.'
        except KeyError:
            error = 'Make sure check out date is not the same as or prior to check in date.'
    return {
        "hotel_info": final_info,
        "error": error
    }


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
