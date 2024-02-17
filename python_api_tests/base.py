import time
import hmac
import requests
import httpx
from urllib import request, parse
import hashlib
import hmac

class BaseTester:
    def __init__(self, apiKey, secret):
        self.apiKey = apiKey
        self.secret = secret
        self.base_url = "https://fapi.binance.com"

    # Public Get requests:
    def get_order_book(self, symbol):
        raise NotImplementedError
    

    def get_premium_index(self, symbol):
        raise NotImplementedError
    

    # Private Get requests:
    def get_account_info(self):
        raise NotImplementedError
    

    # Post requests
    def create_order(self, symbol, side, price, quantity, order_type="LIMIT"):
        raise NotImplementedError
        

    # Delete reqeusts
    def cancel_order(self, symbol, ordId):
        raise NotImplementedError
    
    
    def _get_final_url(self, data, endpoint):
        data["timestamp"] = int(time.time() * 1000)
        data["recvWindow"] = 5000
        query_params = parse.urlencode(data)
        signature = hmac.new(bytes(self.secret , 'utf-8'), bytes(query_params, 'utf-8'), hashlib.sha256).hexdigest()
        final_url = f"{self.base_url}{endpoint}?{query_params}&signature={signature}"
        return final_url