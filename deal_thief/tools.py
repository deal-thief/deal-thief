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


def create_parsed_hotel_info(hotels):
    """Create usable hotel info."""
    price_info = hotels["hotels_prices"]
    name_info = hotels["hotels"]
    hotel_data = []
    for idx in range(len(price_info)):
        hotel_data.append({"id": price_info[idx]["id"],
         "nightly_price": price_info[idx]["agent_prices"][0]["price_per_room_night"],
         "price_total": price_info[idx]["agent_prices"][0]["price_total"],
         "booking_deeplink": price_info[idx]["agent_prices"][0]["booking_deeplink"]
         })
    for idx in range(len(hotel_data)):
        hotel_data[idx]["name"] = name_info[idx]["name"]
        hotel_data[idx]["description"] = name_info[idx]["description"]
        hotel_data[idx]["address"] = name_info[idx]["address"]
        hotel_data[idx]["latitude"] = name_info[idx]["latitude"]
        hotel_data[idx]["longitude"] = name_info[idx]["longitude"]
        hotel_data[idx]["star_rating"] = name_info[idx]["star_rating"]
    return hotel_data
