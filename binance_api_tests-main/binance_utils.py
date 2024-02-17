import urllib.parse
import requests
import hmac
import time
import hashlib



def bn_api_get(api_key, secret_key, url, path, params):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-MBX-APIKEY': api_key
    }
    query_string = urllib.parse.urlencode(params)
    params['signature'] = hmac.new(secret_key.encode(), msg=query_string.encode(), digestmod=hashlib.sha256).hexdigest()
    path = path + '?' + urllib.parse.urlencode(params)
    s = requests.Session()
    # new_source = source.SourceAddressAdapter(OUTIP)
    # s.mount('http://', new_source)
    # s.mount('https://', new_source)
    resp = s.get(url+path, headers=headers)
    # print(resp)
    if resp.status_code == 200:
        return resp.json()

def bn_api_post(api_key, secret_key, url, path, params):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-MBX-APIKEY': api_key
    }
    query_string = urllib.parse.urlencode(params)
    params['signature'] = hmac.new(secret_key.encode(), msg=query_string.encode(), digestmod=hashlib.sha256).hexdigest()
    path = path + '?' + urllib.parse.urlencode(params)
    s = requests.Session()
    # new_source = source.SourceAddressAdapter(OUTIP)
    # s.mount('http://', new_source)
    # s.mount('https://', new_source)
    resp = s.post(url+path, headers=headers)
    # print(resp.json())
    if resp.status_code == 200:
        return resp.json()

def bn_api_delete(api_key, secret_key, url, path, params):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-MBX-APIKEY': api_key
    }
    query_string = urllib.parse.urlencode(params)
    params['signature'] = hmac.new(secret_key.encode(), msg=query_string.encode(), digestmod=hashlib.sha256).hexdigest()
    path = path + '?' + urllib.parse.urlencode(params)
    s = requests.Session()
    # new_source = source.SourceAddressAdapter(OUTIP)
    # s.mount('http://', new_source)
    # s.mount('https://', new_source)
    resp = s.delete(url+path, headers=headers)
    # print(resp.json())
    if resp.status_code == 200:
        return resp.json()

def bn_api_put(api_key, secret_key, url, path, params):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-MBX-APIKEY': api_key
    }
    query_string = urllib.parse.urlencode(params)
    params['signature'] = hmac.new(secret_key.encode(), msg=query_string.encode(), digestmod=hashlib.sha256).hexdigest()
    path = path + '?' + urllib.parse.urlencode(params)
    s = requests.Session()
    # new_source = source.SourceAddressAdapter(OUTIP)
    # s.mount('http://', new_source)
    # s.mount('https://', new_source)
    resp = s.put(url+path, headers=headers)
    # print(resp.json())
    if resp.status_code == 200:
        return resp.json()


