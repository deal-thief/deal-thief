from pyramid.view import notfound_view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    """Render custom not found view."""
    request.response.status = 404
    return {}


@forbidden_view_config()
def forbidden_view(request):
    """Redirect to login if forbidden error received."""
    return HTTPFound(location=request.route_url('login'))
