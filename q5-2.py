
from dotenv import load_dotenv
import json
import websocket
load_dotenv()
from prometheus_client import Gauge, Histogram, start_http_server, Summary, Info

# info = Info('symbol_info', 'Informaton about a symbol high low and delta')
# summary = Summary("priceSpread", "value of priceSpread")
# h= Histogram("priceSpread", "value of priceSpread")
g= Gauge("bnbPriceSpread", "value of priceSpread")
g2= Gauge("bnbAbsDelta", "value of delta")

socket2 = 'wss://stream.binance.com:9443/ws/bnbusdt@kline_1m'

prev=0
current=0
counter=0

def on_message(ws, message):
    data = json.loads(message)
    priceSpread = (float(data['k']['h']) - float(data['k']['l']))
    global current
    global prev 
    current = priceSpread
    delta = current - prev
    global counter
    result={}
    # if counter%10 == 0:
        # info.info({'symbol': data['s'], 'priceSpread': str(priceSpread), 'abs-delta': str(abs(delta)) })
    # summary.observe(priceSpread)
    g.set(priceSpread)
    g2.set(abs(delta))
    print(data['s'], priceSpread, delta, abs(delta), counter)
    counter +=1
    prev=current
    # print(data)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Opened connection")

ws = websocket.WebSocketApp(socket2, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close )

start_http_server(8001)
ws.run_forever()

# @app.route("/metrics")
# def metrics():
#     return ("abc")

# if __name__ == "__main__":
#     app.run(port=8080)
#     ws.run_forever()