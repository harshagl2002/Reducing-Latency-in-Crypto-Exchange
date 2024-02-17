# coding: utf-8
from binance_utils import bn_api_post, bn_api_delete
import time
from datetime import datetime
import numpy as np

api_key = 'xx'
secret_key = 'xx'


usdt_url = 'https://fapi.binance.com'
# usdt_url = 'https://fapi14.binance.com'

def limit_order(pair, side, price, amount):
    r = bn_api_post(api_key, secret_key, usdt_url, '/fapi/v1/order', {'symbol': pair, 'side': side, 'type': 'LIMIT', 'quantity': amount,
                                                                      'price': price, 'timeInForce': "GTC", 'recvWindow': 1000, 'timestamp': int(time.time() * 1000)})
    return r


def post_only(pair, side, price, amount):
    r = bn_api_post(api_key, secret_key, usdt_url, '/fapi/v1/order', {'symbol': pair, 'side': side, 'type': 'LIMIT', 'quantity': amount,
                                                                      'price': price, 'timeInForce': "GTX", 'recvWindow': 1000, 'timestamp': int(time.time() * 1000)})
    return r


def ioc_order(pair, side, price, amount):
    r = bn_api_post(api_key, secret_key, usdt_url, '/fapi/v1/order', {'symbol': pair, 'side': side, 'type': 'LIMIT', 'quantity': amount,
                                                                      'price': price, 'timeInForce': "IOC", 'recvWindow': 1000, 'timestamp': int(time.time() * 1000)})
    return r


def cancel_all(pair):
    r = bn_api_delete(api_key, secret_key, usdt_url, '/fapi/v1/allOpenOrders',
                      {'symbol': pair, 'recvWindow': 1000, 'timestamp': int(time.time() * 1000)})
    return r

post_only_sum = []
ioc_order_sum = []
cancel_all_sum = []
count = 0

while count < 100:
    post_only_start = datetime.now()
    print(post_only_start, 'start post buy order')
    post_only("BTCUSDT", "BUY", 27200, 0.001)
    post_only_end = datetime.now()
    print(post_only_end, 'end post buy order')
    post_only_sum.append(post_only_end - post_only_start)

    ioc_order_start = datetime.now()
    print(ioc_order_start, 'start ioc buy order')
    ioc_order('BTCUSDT', 'BUY', 27200, 0.001)
    ioc_order_end = datetime.now()
    print(ioc_order_end, 'end ioc buy order')
    ioc_order_sum.append(ioc_order_end - ioc_order_start)

    cancel_all_start = datetime.now()
    print(cancel_all_start, 'start cancel order')
    cancel_all("BTCUSDT")
    cancel_all_end = datetime.now()
    print(cancel_all_end, 'end cancel order')
    cancel_all_sum.append(cancel_all_end - cancel_all_start)

    time.sleep(1)
    print(count)
    count += 1

print('post_only_sum:', np.sum(post_only_sum), ' average:', np.mean(post_only_sum), ' median:', np.median(post_only_sum),
      ' 25:', np.percentile(post_only_sum, 25), ' 75:', np.percentile(post_only_sum, 75))
print('ioc_order_sum:', np.sum(ioc_order_sum), ' average:', np.mean(ioc_order_sum), ' median:', np.median(ioc_order_sum),
      ' 25:', np.percentile(ioc_order_sum, 25), ' 75:', np.percentile(ioc_order_sum, 75))
print('cancel_all_sum:', np.sum(cancel_all_sum), ' average:', np.mean(cancel_all_sum), ' median:', np.median(cancel_all_sum),
      ' 25:', np.percentile(cancel_all_sum, 25), ' 75:', np.percentile(cancel_all_sum, 75))

# print(limit_order("EOSUSDT", "BUY", "1.05", "10"))
# print(post_only("EOSUSDT", "BUY", "1.07", "10"))
# print(ioc_order('BTCUSDT', 'BUY', 22000, 0.001))
# print(ioc_order('ETHUSDT', 'BUY', 1200, 0.01))
