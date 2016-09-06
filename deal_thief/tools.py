import os
BASE_URL = 'http://partners.api.skyscanner.net/apiservices/hotels/'
SESSION_BASE_URL = 'http://partners.api.skyscanner.net'

def create_url_for_api_location_id(location):
    """Create url to get location id."""
    SKYSCANNER_API_KEY = os.environ.get('SKYSCANNER_API_KEY')
    result = BASE_URL + 'autosuggest/v2/US/USD/en-US/' + location + '?apikey=' + SKYSCANNER_API_KEY
    return result

def create_url_for_hotel_list(location, checkin, checkout):
    """Create url to get session hotel list."""
    SKYSCANNER_API_KEY = os.environ.get('SKYSCANNER_API_KEY')
    checkin_lst = checkin.split('/')
    checkin_lst = [checkin_lst[2], checkin_lst[0], checkin_lst[1]]
    checkin = '-'.join(checkin_lst)
    checkout_lst = checkout.split('/')
    checkout_lst = [checkout_lst[2], checkout_lst[0], checkout_lst[1]]
    checkout = '-'.join(checkout_lst)
    result = BASE_URL + 'liveprices/v2/US/USD/en-US/' + location + '/' + checkin + '/' + checkout + '/2/1?apiKey=' + SKYSCANNER_API_KEY
    return result


def create_url_for_hotel_details(session_location_header):
    """Create url to get hotel details."""
    result = SESSION_BASE_URL + session_location_header
    return result


def create_url_hotel_id_list(hotel_list_id):
    """Create hotel list to go into url."""
    new_hotel_list_id = ''
    for idx in range(len(hotel_list_id)):
        new_hotel_list_id += str(hotel_list_id[idx]['id']) + ','
    return new_hotel_list_id[:-1]

def create_deep_link_url(hotel_ids, session_location_header):
    """Create final url for deep link."""
    session_and_key = session_location_header.split('/')[-1]
    return SESSION_BASE_URL + '/apiservices/hotels/livedetails/v2/details/' + session_and_key + '&hotelIds=' + hotel_ids