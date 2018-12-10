import requests
import websocket
import threading
import simplejson
from time import sleep
from Classes import cSetUpEntorno as cSetup
from itertools import count #itertools es para contar la cantidad de instancias de una clase


from Classes import cPrintToGoogleSheets as gs
jsonFile='C:/Users/pauli/Documents/Python Projects/ROFEXv2/Classes/client_rofex.json'
#jsonFile='C:/Users/pseoane/Documents/Python Projects/ROFEX Office/Classes/client_rofex.json'
b=gs.cGoogleSetup(jsonFile,"ROFEX-API")

#1
class cSuscription():
    _ids = count(0)

    def __init__(self, user,symbols):
        self.id = next(self._ids)  # se cuenta la cantidad de instancias de una clase para imprimir en gsheets
        self.user=user
        self.symbols=symbols
        self.messages=[]
        self.md=[]
        self.numMessages=0

        self.runWS()

    def p(self):
        print("Cantidad Productos Suscriptos",self.id+1," ", self.user.token)

    def runWS(self):
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
                #print("Receiving...", )

                sleep(1)  # y nada

    def on_message(self, message):
        self.numMessages += 1
        try:
            # Valido Mensaje entrante
            self.msg = simplejson.loads(message)
            self.messages.append(self.msg)

            msgType = self.msg['type'].upper()

            if msgType == 'MD':

                self.incomingMD()
                #self.goRobot()


            elif msgType == 'OR':
                print("En Mensaje OR")
                print(self.msg)
            else:
                print("Tipo de Mensaje Recibido No soportado: " + self.msg)
        except:
            # print("Error al procesar mensaje recibido:--->>> " + msg)
            print("Error al procesar mensaje recibido:--->>> " + self.msg)

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


    def incomingMD(self):

        self.timestamp = self.msg['timestamp']
        self.sym = self.msg['instrumentId']['symbol']
        # Aca hay un problema si no hay bid u offer pq solo viene ['marketData']
        self.bidMsg = self.msg['marketData']['BI']
        self.offerMsg = self.msg['marketData']['OF']

        if self.bidMsg == []:
            # >No BID detected")
            self.bid = 0
            self.bidSize = 0
        else:
            self.bid = self.msg['marketData']['BI'][0]['price']
            self.bidSize = self.msg['marketData']['BI'][0]['size']

        if self.offerMsg == []:
            # >No OFFER detected")
            self.offer = 0
            self.offerSize = 0
        else:
            self.offer = self.msg['marketData']['OF'][0]['price']
            self.offerSize = self.msg['marketData']['OF'][0]['size']


        self.md.append([self.timestamp,self.sym,self.bid,self.offer,self.bidSize,self.offerSize,self.numMessages])
        #print("MD Array :",self.md[-1])
        #return


    def getBid(self):
        return self.bid

    def getBidSize(self):
        return self.bidSize

    def getOffer(self):
        return self.offer

    def getOfferSize(self):
        return self.offerSize


    def goRobot(self):

        print("En goRobot***->",len(self.md),self.numMessages,"--",self.sym,"-->",self.bid,"/",self.offer,"    ",self.bidSize,"/",self.offerSize)
        #print(self.md[-1][2])


        #for col in range(6):

        #gs.cPrintRangeToGSheets(b.sheet,10,1,["Celda 1","Celda 2"])
        #gs.cPrintToGSheets(b.sheet, 1, 1, "Hello Class 2.7")
        #worker=threading.Thread(target=self.printAIOinGS)
        #worker=threading.Timer(10,self.printAIOinGS) #timer 1 seg
        #worker.start()




        #-------------
        # en esta version usa un worker por cada celda
        #for col in range (5):

        #    worker = threading.Thread(target=gs.cPrintToGSheets,args=(b.sheet,self.id+3,col+1,self.md[-1][col+1]))
            #worker = threading.Timer(1, gs.cPrintToGSheets, args=[b.sheet, self.id+3, 1, self.numMessages])

        #    worker.start()
        #----------------
        return

    def printAIOinGS(self):
        #en esta version usa un solo worker para toda la fila
        # TODO: armar la escritura del rango para usar menos quota en vez de la fila
        for col in range (6):
            gs.cPrintToGSheets(b.sheet,self.id+3,col+1,self.md[-1][col+1])

