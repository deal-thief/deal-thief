from pyramid.view import view_config
from ..models import User, Search


@view_config(route_name='home', renderer='../templates/home.html')
def home_view(request):
    return {}
