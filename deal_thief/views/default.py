from pyramid.view import view_config
from ..models import User, Search
from datetime import datetime
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

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
    # location = checkin = checkout = error = ''
    # if request.method == "POST":
    #     location = request.params.get('location', '')
    #     checkin = request.params.get('checkin', '')
    #     checkout = request.params.get('checkout', '')
    #     if not location or not checkin or not checkout:
    #         error = 'Location Checkin and Chckout are required'
    import pdb; pdb.set_trace()
    built = [request.params['location'], request.params['start'], request.params['end']]
    return {}
