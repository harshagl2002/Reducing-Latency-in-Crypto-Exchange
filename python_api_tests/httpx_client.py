import httpx
from python_api_tests.base import BaseTester
import time

class HttpxClient(BaseTester):
    def __init__(self, apiKey, secret):
        super().__init__(apiKey, secret)
        self.client = httpx.Client()
        self.name = "httpx"

    def get_premium_index(self, symbol):
        endpoint = "/fapi/v1/premiumIndex"
        data = {"symbol": symbol}
        return self._get_request(data, endpoint)
    
    def get_order_book(self, symbol):
        endpoint = "/fapi/v1/depth"
        data = {"symbol": symbol}
        return self._get_request(data, endpoint)
    
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

    
    # Helper Methods
    def _get_request(self, data, endpoint):
        final_url = self._get_final_url(data, endpoint)
        response = self.client.get(final_url, headers={"X-MBX-APIKEY": self.apiKey})
        return response.json()
    
    def _post_request(self, data, endpoint):
        final_url = self._get_final_url(data, endpoint)
        response = self.client.post(final_url, headers={"X-MBX-APIKEY": self.apiKey})
        return response.json()
    
    def _delete_request(self, data, endpoint):
        final_url = self._get_final_url(data, endpoint)
        response = self.client.delete(final_url, headers={"X-MBX-APIKEY": self.apiKey})
        return response.json()