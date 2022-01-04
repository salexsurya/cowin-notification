"""Module containing API calls."""
from functools import lru_cache
import requests
import os

import pandas as pd


class API():
    """Class to handle API calls from COWIN site. Refer: https://apisetu.gov.in/public/marketplace/api/cowin#/ ."""

    def __init__(self) -> None:
        """Class to handle API calls from COWIN site."""
        self._header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    def get_states(self) -> pd.DataFrame:
        """State id and names."""
        url = f"https://cdn-api.co-vin.in/api/v2/admin/location/states"
        with requests.session() as session:
            response = session.get(url, headers=self._header)
            data = response.json()
            return pd.json_normalize(data, 'states')

    def get_districts(self, state_id: str) -> pd.DataFrame:
        """State id and names."""
        url = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}"
        with requests.session() as session:
            response = session.get(url, headers=self._header)
            data = response.json()
            return pd.json_normalize(data, 'districts')

    def get_session_by_pincode(self, pincode: int, sdate: str) -> pd.DataFrame:
        """Get available session by pin and date."""
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={sdate}"
        with requests.session() as session:
            response = session.get(url, headers=self._header)
            data = response.json()
            # df = pd.json_normalize(data, 'districts')
            return None # to be implemented

    def get_session_by_district(self, district_id: int, sdate: str) -> pd.DataFrame:
        """Get available session by dist id and date."""
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={district_id}&date={sdate}"
        with requests.session() as session:
            response = session.get(url, headers=self._header)
            data = response.json()
            # df = pd.json_normalize(data, 'districts')
            return None # to be implemented

    def get_session_by_latlong(self, lat: float, long: float) -> pd.DataFrame:
        """Get available session by lat, long and date."""
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByLatLong?lat={lat}&long={long}"
        with requests.session() as session:
            response = session.get(url, headers=self._header)
            data = response.json()
            # df = pd.json_normalize(data, 'districts')
            return None # to be implemented

    def get_appointment_by_pincode(self, pincode: int, sdate: str) -> pd.DataFrame:
        """Get available appointment by pin and date."""
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={sdate}"
        with requests.session() as session:
            response = session.get(url, headers=self._header)
            data = response.json()
            meta = ['center_id', 'name', 'address', 'state_name', 'district_name',
                    'block_name', 'pincode', 'lat', 'long', 'from', 'to', 'fee_type']
            df = pd.json_normalize(data['centers'], record_path='sessions', meta=meta)
            df = df.drop(columns=['session_id', 'state_name', 'block_name', 'from', 'to', 'lat', 'long', 'slots'])\
                .reset_index(drop=True)\
                .rename(columns={'name': 'center_name'})
            return df

    @lru_cache(maxsize=None)
    def get_appointment_by_district(self, district_id: int, sdate: str) -> pd.DataFrame:
        """Get available appointment by dist and date."""
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={sdate}"
        with requests.session() as session:
            response = session.get(url, headers=self._header)
            data = response.json()
            meta = ['center_id', 'name', 'address', 'state_name', 'district_name',
                    'block_name', 'pincode', 'lat', 'long', 'from', 'to', 'fee_type']
            df = pd.json_normalize(data['centers'], record_path='sessions', meta=meta)
            if len(df) > 0:
                df = df.drop(columns=['session_id', 'state_name', 'block_name', 'from', 'to', 'lat', 'long', 'slots'])\
                    .reset_index(drop=True)\
                    .rename(columns={'name': 'center_name'})
                return df
            return pd.DataFrame()

    def get_appointment_by_center_id(self, center_id: int, sdate: str) -> pd.DataFrame:
        """Get available appointment by center id and date."""
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByCenter?center_id={center_id}&date={sdate}"
        with requests.session() as session:
            response = session.get(url, headers=self._header)
            data = response.json()
            meta = ['center_id', 'name', 'address', 'state_name', 'district_name',
                    'block_name', 'pincode', 'lat', 'long', 'from', 'to', 'fee_type']
            df = pd.json_normalize(data['centers'], record_path='sessions', meta=meta)
            df = df.drop(columns=['session_id', 'state_name', 'block_name', 'from', 'to', 'lat', 'long', 'slots'])\
                .reset_index(drop=True)\
                .rename(columns={'name': 'center_name'})
            return None # to be implemented
