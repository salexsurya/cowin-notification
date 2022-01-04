"""Module containing API calls."""
import requests

import pandas as pd
import os
from urllib.parse import quote

gmid = 'czzhxx'
pwd = quote('iBorn$@nk1982Ag') 
#http://GMID:PASSWORD@naproxy.gm.com:80
proxy = f"http://{gmid}:{pwd}@naproxy.gm.com:80"
#proxy = f"http://gmioproxy.gm.com:80/"
os.environ['http_proxy'] = proxy 
# os.environ['HTTP_PROXY'] = proxy #+ ":80"
os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy #+ ":443"

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=561&date=17-05-2021"
with requests.session() as session:
    response = session.get(url, headers=header) # , proxies=self._proxies
    data = response.json()
    meta = ['center_id', 'name', 'address', 'state_name', 'district_name',
            'block_name', 'pincode', 'lat', 'long', 'from', 'to', 'fee_type']
    df = pd.json_normalize(data['centers'], record_path='sessions', meta=meta)
    df = df.drop(columns=['session_id', 'state_name', 'block_name', 'from', 'to', 'lat', 'long', 'slots'])\
        .reset_index(drop=True)\
        .rename(columns={'name': 'center_name'})
    print(df.index)