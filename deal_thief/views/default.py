from pyramid.view import view_config
from ..models import User, Search
from datetime import datetime
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests

@view_config(route_name='home', renderer='../templates/home.html')
def home_view(request):
    slider = {

    }
    return {
        'page_title': 'Home',
        'today_date': datetime.now().strftime("%Y-%m-%d")
    }


@view_config(route_name='login', renderer='../templates/login.html')
def login_view(request):
    return {
        'page_title': 'Login',
    }


@view_config(route_name='search', renderer='../templates/search.html')
def search_view(request):
    """Give us our search view."""
    from ..tools import create_url_for_api_location_id
    location = request.params['location']
    checkin = request.params['start']
    checkout = request.params['end']
    location_id_url = create_url_for_api_location_id(location)
    location_id_unparsed = requests.get(location_id_url)
    location_id = location_id_unparsed['results'][0]['individual_id']
    import pdb; pdb.set_trace()
    return {}
