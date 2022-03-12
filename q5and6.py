
from dotenv import load_dotenv
import json
from numpy import spacing
import websocket
load_dotenv()
from prometheus_client import Gauge, Histogram, start_http_server, Summary, Info

g= Gauge("priceSpread", "value of priceSpread", ['symbols'])
g2= Gauge("absDelta", "value of delta")

ws = websocket.create_connection("wss://stream.binance.com:9443/ws")
ws.send(json.dumps({
  "method": "SUBSCRIBE",
  "params": [
    "btcusdt@kline_1m",
    "bnbusdt@kline_1m",
    "ethusdt@kline_1m",
    "dogeusdt@kline_1m",
    "xrpusdt@kline_1m"
  ],
  "id": 1
}))

prev=0
current=0
counter=0

def on_message(message):
    data = json.loads(message)
    if 'k' not in data:
        pass
    else:
        priceSpread = (float(data['k']['h']) - float(data['k']['l']))
        global current
        global prev 
        current = priceSpread
        delta = current - prev
        global counter
        if counter%10 == 0:
            g.labels(f"{data['s']}-priceSpread").set(priceSpread)
            g.labels(f"{data['s']}-delta").set(abs(delta))
            print(data['s'], priceSpread, delta, abs(delta), counter)
        counter +=1
        prev=current

start_http_server(8000)

while True:
    result = ws.recv()
    on_message(result)

ws.close()