import requests
import websocket
import threading
import simplejson

from time import sleep
from Classes import cSetUpEntorno as cSetup
from itertools import count #itertools es para contar la cantidad de instancias de una clase

from Classes import cRofexMessage as rMsg
from Classes import cPrintToGoogleSheets as gs
path='C:/Users/pauli/'
# path='C:/Users/pseoane/'

jsonFile=path+'Documents/Python Projects/ROFEXv2/Classes/client_rofex.json'
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

        self.bid=0
        self.offer=0
        self.bidSize=0
        self.offerSize=0
        self.numMessages=0
        self.timestamp=0
        self.indexBid=0
        self.indexOffer=0
        self.sym=""


        #for goRobot2 2D Array or list of lists for storing the latest message of each contract
        width=10
        heigth=len(symbols)
        self.matrix=[[0 for x in range(width)] for y in range(heigth)]

        self.runWS()

    def p(self):
        print("Cantidad Productos Suscriptos",self.id+1," ", self.user.token)

    def runWS(self):
        headers = {'X-Auth-Token:{token}'.format(token=self.user.token)}
        ws = websocket.WebSocketApp(self.user.activeWSEndpoint,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         header=headers)

        wst = threading.Thread(target=ws.run_forever, kwargs={"ping_interval": 5})
        wst.start()
        # Esperamos a que la conexion ws se establezca
        conn_timeout = 5
        # conn_timeout = 50 #y nada
        sleep(1)

        while not ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
        else:
            i=0
            for self.sym in self.symbols:
                self.matrix[i][0]=self.sym
                i+=1


                aaa = self.buildMessage()
                ws.send(aaa)

                print("Sent Suscription msg", self.sym)
                #print("Receiving...", )

                sleep(1)  # y nada

    def on_message(self, message):
        self.numMessages += 1

        try:

            # -----------------------
            print("Test rTEST")
            rTEST = rMsg.cRofexMessage(message)
            #self.rTEST.getLastMessage()
            # self.md.append(rTEST.getLastMessage())
            # print("rTEST last Message: ",self.md)


            # -----------------------

            # Valido Mensaje entrante
            self.msg = simplejson.loads(message)
            self.messages.append(self.msg)
            #print("En cSuscript",self.msg)

            msgType = self.msg['type'].upper()

            if msgType == 'MD':

                self.incomingMD()
                self.updateMatrix()
                self.goRobot2()


            elif msgType == 'OR':
                print("En Mensaje OR")
                print(self.msg)
            else:
                print("Tipo de Mensaje Recibido No soportado: " + self.msg)
        except:
            # print("Error al procesar mensaje recibido:--->>> " + msg)
            print("Error al procesar mensaje recibido:--->>> ", self.msg)

    def on_error(self, error):
        print("Salio por error: ",error)
        self.ws.close()

    def on_close(ws):
        print("### connection closed ###")

    def on_open(ws):
        pass
        #print("WS Conection Open...")


    def buildMessage(self):
        return "{\"type\":\"" + self.user.type_ + "\",\"level\":" + self.user.level_ + ", \"entries\":[\"BI\", \"OF\"],\"products\":[{\"symbol\":\"" + self.sym + "\",\"marketId\":\"" + self.user.marketId_ + "\"}]}"


    def incomingMD(self):

        self.timestamp = self.msg['timestamp']
        self.sym = self.msg['instrumentId']['symbol']
        # Aca hay un problema si no hay bid u offer pq solo viene ['marketData']
        bidMsg = self.msg['marketData']['BI']
        offerMsg = self.msg['marketData']['OF']

        if bidMsg != []:

            self.bid = self.msg['marketData']['BI'][0]['price']
            self.bidSize = self.msg['marketData']['BI'][0]['size']

        if offerMsg != []:

            self.offer = self.msg['marketData']['OF'][0]['price']
            self.offerSize = self.msg['marketData']['OF'][0]['size']


        self.md.append([self.timestamp,self.sym,self.bid,self.offer,self.bidSize,self.offerSize,self.numMessages])
        #print("MD Array :",self.md[-1])
        #return
        print("Ok Incoming MD:")

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

    def updateMatrix(self):
        row = self.symbols.index(self.sym)
        # update that row
        self.matrix[row][1] = self.bid
        self.matrix[row][2] = self.offer
        self.matrix[row][3] = self.bidSize
        self.matrix[row][4] = self.offerSize
        self.matrix[row][5] = self.numMessages
        self.matrix[row][6] = self.timestamp
        #return

    def goRobot2(self):
        #buscar en row de la matrix loe corresponde a ese mensaje
        #row= self.symbols.index(self.sym)
        #update that row
        #self.matrix[row][1]=self.bid
        #self.matrix[row][2]=self.offer
        #self.matrix[row][3]=self.bidSize
        #self.matrix[row][4]=self.offerSize
        #self.matrix[row][5] = self.numMessages
        #self.matrix[row][6] = self.timestamp

        print("En goRobot 2******->\n", self.matrix,"\n")

        if self.matrix[0][2] !=0:
            self.indexBid=self.matrix[1][1]/self.matrix[0][2]

        if self.matrix[0][1] !=0:
            self.indexOffer=self.matrix[1][2]/self.matrix[0][1]


        if self.matrix[0][2] !=0 and self.matrix[1][1] !=0:
            self.availableBid = round(min(self.matrix[1][1] * self.matrix[1][3] / self.matrix[0][2] / 1000,
                                self.matrix[0][2] * self.matrix[0][4] * 1000 / self.matrix[1][1]),2)

        if self.matrix[0][1] != 0 and self.matrix[1][2] !=0:
            self.availableOffer = round(min(self.matrix[1][2] * self.matrix[1][4] / self.matrix[0][1] / 1000,
                                  self.matrix[0][1] * self.matrix[0][3] * 1000 / self.matrix[1][2]),2)

        self.midMarket      = (self.indexBid+self.indexOffer)/2

        print("Index en USD: ",self.indexBid," / ",self.indexOffer,"size :",str(self.availableBid) , "x", str(self.availableOffer),"----->",str(round(self.midMarket*0.995,2)),"/",str(round(self.midMarket*1.005,2))," SIZE:----> " ,str(round(self.availableBid,0)),"xx",str(round(self.availableOffer,0)))

       # print("Available Size: ",)
        #print ("Size       : ", self.matrix[1][3],self.matrix[0][4], " / ", self.matrix[1][4],self.matrix[0][3])

        # return


    def printAIOinGS(self):
        #en esta version usa un solo worker para toda la fila
        # TODO: armar la escritura del rango para usar menos quota en vez de la fila
        for col in range (6):
            gs.cPrintToGSheets(b.sheet,self.id+3,col+1,self.md[-1][col+1])

