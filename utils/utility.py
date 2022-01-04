"""Utility functions."""
from functools import lru_cache
import json
from os import path
import requests

# import googlemaps
import pandas as pd
import numpy

def load_districts() -> pd.DataFrame:
    """Return district name and id with respective state name."""
    district_filename = './libs/districts.csv'
    if path.exists(district_filename):
        # If file exists, load
        return pd.read_csv(district_filename)
    else:
        # If file doesn't exist, pull district data
        states = api.get_states()
        districts = pd.DataFrame()
        for state_id, state_name in zip(states.state_id.tolist(), states.state_name.tolist()):
            district = api.get_districts(state_id)
            district = district.assign(state_id=state_id,
                                       state_name=state_name)
            districts = districts.append(district, ignore_index=True)
        districts = districts.reindex(
            columns=['state_id', 'state_name', 'district_id', 'district_name'])
        districts.to_csv(district_filename, index=False)
        return districts

def get_district_id(districts: pd.DataFrame, district_name: str) -> int:
    """Return district id for given district name."""
    s = districts.loc[(districts.district_name == district_name), 'district_id']\
        .reset_index(drop=True)
    return s.at[0]

def sms(phone_numbers: str, message: str) -> str:
    """Send SMS to users."""
    # mention url
    url = "https://www.fast2sms.com/dev/bulkV2"

    # Create payload
    payload = {
        'sender_id': 'TXTIND',
        'message': message,
        'language': 'english',
        'route': 'v3',
        'flash': '0',
        'numbers': phone_numbers
    }

    # Header
    headers = {
        'authorization': 'ewP1DxEb6WZV8iAyRS9CH2BvYstdKgJnXU4MFfqk3roIpzmjhLozUYXEA9ncJlt1p7fNdu0D2LmsZBOh',
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }

    # make a post request
    response = requests.request("POST", url, data=payload, headers=headers)

    # confirm
    if response.status_code == 200:
        returned_msg = json.loads(response.text)
        print(returned_msg['message'])

@lru_cache(maxsize=None)
def find_dist_between(origins: str, destination: str) -> float:
    # Requires API key
    gmaps = googlemaps.Client(key='AIzaSyD9TRihmyM-ripUM99PxPwF77oXJpnvvlw')
    
    # Requires cities name
    my_dist = gmaps.distance_matrix(origins, destination)['rows'][0]['elements'][0]
    
    # Printing the result
    return my_dist['distance']['text']
