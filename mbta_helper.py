import json
import urllib.request
from urllib.parse import urlencode
from urllib.parse import quote

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MAPBOX_TOKEN = 'pk.eyJ1IjoibWlrZWJvenphIiwiYSI6ImNsaDN1ejllNzBlZnozZXAzOGQzN2t4YTgifQ.nq1WX9DuSrH4Fw9jOZ6v8w'

MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
MBTA_API_KEY = '2eb2b9cb49de41a3a8c96912bbd705e6'

def build_mapbox_url(query):
    encoded_query = quote(query)
    params = {'access_token': MAPBOX_TOKEN, 'types': 'poi'}
    encoded_params = urlencode(params)
    return f"{MAPBOX_BASE_URL}/{encoded_query}.json?{encoded_params}"

def get_lat_lng(query):
    url = build_mapbox_url(query)
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode('utf-8')
        response_data = json.loads(response_text)

    lat = response_data['features'][0]['geometry']['coordinates'][1]
    lng = response_data['features'][0]['geometry']['coordinates'][0]

    return lat, lng

def get_nearest_mbta_stop(lat, lng,transportation_type):
    route_type_map = {
      'bus': 3,
      'commuter_rail': 2,
      'subway': 0
    }
  
    params = {
        'api_key': MBTA_API_KEY,
        'sort': 'distance',
        'filter[latitude]': lat,
        'filter[longitude]': lng,
        'filter[route_type]': route_type_map[transportation_type]
    }

    encoded_params = urlencode(params)
    url = f"{MBTA_BASE_URL}?{encoded_params}"

    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode('utf-8')
        response_data = json.loads(response_text)

    closest_stop = response_data['data'][0]
    stop_name = closest_stop['attributes']['name']
    wheelchair_accessible = closest_stop['attributes']['wheelchair_boarding']

    return stop_name, wheelchair_accessible

def find_stop_near(location,transportation_type):
    lat, lng = get_lat_lng(location)
    stop_name, wheelchair_accessible = get_nearest_mbta_stop(lat, lng,transportation_type)
    return stop_name, wheelchair_accessible
