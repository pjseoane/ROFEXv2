import websocket
import threading
import time


def on_message(ws, message):
    # print("weeee",message)
    # msg.append(message)
    lastMessage = message
    print(lastMessage)
    # time.sleep(1)
    # worker1=threading.Thread(target=printToGoogleSheets,args=(sheet,11,1,msg[-1]))
    # worker1=threading.Timer(1.0,printToGoogleSheets,args=[sheet,11,1,lastMessage])
    # worker1=threading.Timer(1,gs.cPrintToGSheets,args=[b.sheet,11,1,lastMessage])

    # worker1.start()


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("WS Open....")

    def run(*args):
        for i in range(50):
            time.sleep(.5)

            ws.send("Hello %d" % i)

        time.sleep(1)
        ws.close()
        print("thread terminating...")

    wst = threading.Thread(target=run)
    wst.start()


if __name__ == "__main__":
    # websocket.enableTrace(True)

    msg = []

    ws = websocket.WebSocketApp("ws://echo.websocket.org/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)

    ws.run_forever()