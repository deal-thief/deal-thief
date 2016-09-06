import os

def create_url_for_api_location_id(location):
    SKYSCANNER_API_KEY = os.environ.get('SKYSCANNER_API_KEY')
    result = 'http://partners.api.skyscanner.net/apiservices/hotels/autosuggest/v2/US/USD/en-US/' + location + '?apikey=' + SKYSCANNER_API_KEY
    return result
