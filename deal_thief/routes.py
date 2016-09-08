"""Routing for the pyramid app."""


def includeme(config):
    """Routing function."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('search', '/search')
    config.add_route('about', '/about')
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('dashboard', '/dashboard')
    config.add_route('profile', '/profile')
