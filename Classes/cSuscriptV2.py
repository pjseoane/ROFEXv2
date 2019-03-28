import websocket
import threading
import Classes.cRofexMessage as rMsg
#from Classes import cRofexMessage as rMsg
from time import sleep
from itertools import count #itertools es para contar la cantidad de instancias de una clase

#
# from Classes import cPrintToGoogleSheets as gs
# #jsonFile='C:/Users/pauli/Documents/Python Projects/ROFEXv2/Classes/client_rofex.json'
# jsonFile='C:/Users/pseoane/Documents/Python Projects/ROFEXv2/Classes/client_rofex.json'
# b=gs.cGoogleSetup(jsonFile,"ROFEX-API")
# #


class cSuscription():
    _ids = count(0)

    def __init__(self, user,symbols):
        self.id = next(self._ids)  # se cuenta la cantidad de instancias de una clase para imprimir en gsheets
        self.user=user
        self.symbols=symbols
        self.messages=[]
        self.md=[]
        self.numMessages=0
        self.rTest=rMsg.cRofexMessage()

        #self.ticker1=ticker1
        #self.ticker2=ticker2
        headers = {'X-Auth-Token:{token}'.format(token=self.user.token)}


        self.ws = websocket.WebSocketApp(self.user.activeWSEndpoint,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         header=headers)

        wst = threading.Thread(target=self.ws.run_forever, kwargs={"ping_interval": 5})
        wst.start()
        # Esperamos a que la conexion ws se establezca
        conn_timeout = 5
        # conn_timeout = 50 #y nada
        sleep(1)

        while not self.ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
        else:

            for self.sym in self.symbols:
                aaa = self.buildMessage(self.sym)
                self.ws.send(aaa)

                print("Sent Suscription msg", self.sym)
                # print("Receiving...", )

                sleep(1)  # y nada


    # def p(self):
    #     print("Cantidad Productos Suscriptos",self.id+1," ", self.user.token)

    #def runWS(self):

    def on_message(self, message):
        self.numMessages += 1
      #  self.rTEST=rMsg.cRofexMessage()
        try:

            print("Test rTEST")
            self.rTEST = rMsg.cRofexMessage(message)
            # self.rTEST.getLastMessage()
            self.md.append(self.rTEST.getLastMessage())


        except:
            # print("Error al procesar mensaje recibido:--->>> " + msg)
            print("Error al procesar mensaje recibido:--->>> " )

    def on_error(self, error):
        print("Salio por error: ",error)
        self.ws.close()

    def on_close(ws):
        print("### connection closed ###")

    def on_open(ws):
        pass
        #print("WS Conection Open...")


    def buildMessage(self, sym):
        return "{\"type\":\"" + self.user.type_ + "\",\"level\":" + self.user.level_ + ", \"entries\":[\"BI\", \"OF\"],\"products\":[{\"symbol\":\"" + sym + "\",\"marketId\":\"" + self.user.marketId_ + "\"}]}"


