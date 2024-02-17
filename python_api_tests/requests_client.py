import requests
from python_api_tests.base import BaseTester
import time

class RequestsClient(BaseTester):
    def __init__(self, apiKey, secret, use_session):
        super().__init__(apiKey, secret)
        self.session = requests.Session()
        self.use_session = use_session
        self.headers = {"X-MBX-APIKEY": self.apiKey}
        if self.use_session:
            self.session.headers.update({"X-MBX-APIKEY": self.apiKey})
        self.name = "requests"

    def get_premium_index(self, symbol):
        endpoint = "/fapi/v1/premiumIndex"
        data = {"symbol": symbol}
        return self._get_request(data, endpoint)
    
    def get_order_book(self, symbol):
        endpoint = "/fapi/v1/depth"
        data = {"symbol": symbol}
        return self._get_request(data, endpoint)
    
    def get_account_info(self):
        endpoint = "/fapi/v2/account"
        return self._get_request({}, endpoint)
    
    def create_order(self, symbol, side, price, quantity, order_type="LIMIT"):
        endpoint = "/fapi/v1/order"
        data = {
            "symbol": symbol,
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity
        }
        if order_type.upper() == "LIMIT":
            data["price"] = price
            data["timeInForce"] = "GTD"
            data["goodTillDate"] = int(time.time() + 650) * 1000
        result = self._post_request(data, endpoint)
        return result["orderId"]
        
    def cancel_order(self, symbol, ordId):
        endpoint = "/fapi/v1/order"
        data = {
            "symbol": symbol,
            "orderId": ordId
        }
        result = self._delete_request(data, endpoint)
        return result
    
    # A method to cancel all orders. This is because sometime cancel order will fail.
    # And we need to clear all the other unhandeled orders.
    def cancel_all_order(self, symbol):
        pass


    # Helper Methods
    def _get_request(self, data, endpoint):
        final_url = self._get_final_url(data, endpoint)
        if self.use_session:
            response = self.session.get(final_url, timeout=10)
        else:
            response = requests.get(final_url, headers=self.headers, timeout=10)
        return response.json()
    
    def _post_request(self, data, endpoint):
        final_url = self._get_final_url(data, endpoint)
        if self.use_session:
            response = self.session.post(final_url, timeout=10)
        else:
            response = requests.post(final_url, headers=self.headers, timeout=10)
        return response.json()

    def _delete_request(self, data, endpoint):
        final_url = self._get_final_url(data, endpoint)
        if self.use_session:
            response = self.session.delete(final_url, timeout=10)
        else:
            response = requests.delete(final_url, headers=self.headers, timeout=10)
        return response.json()
