# Goal
This directory is used to test the latency of Binance exchange api in HTTPS and WebSocket protocals. Currently, only WebSocket is enabled.

# WebSocket
url = f"wss://fstream.binance.com/stream?streams=btcusdt@depth@{freq}ms"
wss://fstream.binance.com/stream is the base url of WebSocket to fetch futures information from Binance Exchange. 
- btcusdt is the instrument id. It denotes usdt-margin Bitcoin perpetual contract.
- depth is the order book depth.
- freq is the update frequency of this stream. It can only be 0, 100, and 500ms. "In order to provide users with more secure and stable services, the update time of <symbol>depth@0ms and <symbol>@depth<level>@0ms 
is dynamically adjusted according to the total amount of data traffic and other objective conditions." Thus, 0ms is actually in live production.

