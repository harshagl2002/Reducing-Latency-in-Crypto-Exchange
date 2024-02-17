import websockets
import asyncio
import json
import numpy as np

def get_latency():
    for fn in ["binance_0ms.json", "binance_100ms.json", "binance_500ms.json"]:
        with open(fn, "r") as fd:
            content = fd.read()
            items = []
            for line in content.split("\n"):
                line = line.strip()
                if not line: continue
                item = json.loads(line)
                items.append(item)
                # Key "E": part of aggregated trade strams. It denotes event timestamp.
            e_series = [item["data"]["E"] for item in items]
            deltas = []
            last_x = e_series[0]
            for x in e_series[1:]:
                delta = x - last_x
                last_x = x
                deltas.append(delta)
            deltas = np.array(deltas)
            mean = np.mean(deltas)
            var = np.var(deltas)
            print(f"Frequency: {fn}")
            print("Delta Mean:", mean)
            print("FrequDelta Variance", var)

async def depth(freq):
    if freq not in [0, 100, 500]:
        return
    url = f"wss://fstream.binance.com/stream?streams=btcusdt@depth@{freq}ms"
    items = []
    async with websockets.connect(url) as websocket:
        for i in range(2000):
            raw_data = await websocket.recv()
            print(raw_data)
            items.append(raw_data)
    data = "".join(["%s\n" % item for item in items])
    with open(f"binance_{freq}ms.json", "w") as fd:
        fd.write(data)

if __name__ == "__main__":
    asyncio.run(depth(0))
    asyncio.run(depth(100))
    asyncio.run(depth(500))
    get_latency()
