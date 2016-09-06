import os

def create_url_for_api_location_id(location):
    """Create url to get location id."""
    SKYSCANNER_API_KEY = os.environ.get('SKYSCANNER_API_KEY')
    result = 'http://partners.api.skyscanner.net/apiservices/hotels/autosuggest/v2/US/USD/en-US/' + location + '?apikey=' + SKYSCANNER_API_KEY
    return result

def create_url_for_hotel_list(location, checkin, checkout):
    """Create url to get session hotel list."""
    SKYSCANNER_API_KEY = os.environ.get('SKYSCANNER_API_KEY')
    result = 'http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/US/USD/en-US/' + location + checkin + checkout + '2/1?apiKey=' + SKYSCANNER_API_KEY
    return result