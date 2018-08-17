#!/usr/bin/python3
import json, time
import websocket

import time
import json
import thread

from threading import Thread

def on_message(ws, message):
    try:

        messageDict = json.loads(message)
        # Check Message Type and Log if the order is filled
        if "type" in messageDict:
            data = messageDict["type"]
            if data == "done" and messageDict["reason"] == "filled":
                print("new Order " + str(messageDict["sequence"]) + ": " )
                print ("Product ID:" + messageDict["product_id"])
                print ("Order ID:" + messageDict["order_id"])
                print ("Price:" + messageDict["price"])
                print ("Side: " + messageDict["side"])
                print("\n")
    except:
        print('An error occurred.')


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("ONOPEN")
    def run(*args):
        # Subscribe for Ticker and OrderBook
        message = {
            "type": "subscribe",
            "channels": [{"name": "full", "product_ids": ["BTC-USD"]}, {"name": "ticker", "product_ids": ["BTC-USD"]}]
        }
        ws.send(json.dumps(message))
        while True:
            time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws-feed.gdax.com",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
