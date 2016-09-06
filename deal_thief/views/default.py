from pyramid.view import view_config
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..security import check_credentials
from ..models import User, Search

@view_config(route_name='home', renderer='../templates/home.html')
def home_view(request):
    slider = {

    }
    return {
        'page_title': 'Home',
        'today_date': datetime.now().strftime("%Y-%m-%d")
    }


@view_config(route_name='register', renderer='../templates/register.html')
def register_view(request):
    first_name = last_name = email = password = city = state = error = ''
    if request.method == 'POST':
        first_name = request.params.get('first-name', '')
        last_name = request.params.get('last-name', '')
        email = request.params.get('email', '')
        password = request.params.get('password', '')
        city = request.params.get('city', '')
        state = request.params.get('state', '')
        if first_name and last_name and email and password and city and state:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=pwd_context.encrypt(password),
                city=city,
                state=state
            )
            request.dbsession.add(new_user)
            return HTTPFound(location=request.route_url('login'))
        else:
            error = 'All fields are required'
    return {
        'page_title': 'Register',
        'error': error
    }


@view_config(route_name='login', renderer='../templates/login.html')
def login_view(request):
    error = ''
    if request.method == 'POST':
        email = request.params.get('email', '')
        password = request.params.get('password', '')
        if email and password:
            query = request.dbsession.query(User).filter_by(email=email)
            stored_user = query.first()
            if stored_user:
                if check_credentials(email, password, stored_user):
                    headers = remember(request, email)
                    return HTTPFound(
                            location=request.route_url('home'),
                            headers=headers
                    )
        error = 'Unsuccessul, try again'

    return {
        'page_title': 'Login',
        'error': error
    }


@view_config(route_name='logout')
def logout_view(request):
    """Clear cookie, log user out and redirect to home_view."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='dashboard', renderer='../templates/dashboard.html', permission='private')
def dashboard_view(request):
    """Dashboard view for user."""
    return {}
