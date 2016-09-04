from pyramid.view import view_config
from ..models import User, Search
from datetime import datetime

@view_config(route_name='home', renderer='../templates/home.html')
def home_view(request):
    return {
        'page_title': 'Home',
        'today_date': datetime.now().strftime("%Y-%m-%d")
    }
