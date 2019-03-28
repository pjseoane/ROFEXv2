from itertools import count #itertools es para contar la cantidad de instancias de una clase
import simplejson

class cRofexMessage():

    _ids = count(0)
    md = []

    def __init__ (self, message):

        self.id = next(self._ids)  # se cuenta la cantidad de instancias de una clase

        self.msg        = simplejson.loads(message)
        self.msgType       = self.msg['type'].upper()

        if self.msgType == 'MD':
            self.incomingMD()
            self.processMessage()

        elif self.msgType == 'OR':
            print("En Mensaje OR")
            print(self.msg)
        else:
            print("Tipo de Mensaje Recibido No soportado: " + self.msg)


    def incomingMD(self):
        timestamp = self.msg['timestamp']
        marketId = self.msg['instrumentId']['marketId']
        sym = self.msg['instrumentId']['symbol']
        # Aca hay un problema si no hay bid u offer pq solo viene ['marketData']
        bidMsg = self.msg['marketData']['BI']
        offerMsg = self.msg['marketData']['OF']

        if not self.bidMsg:
            # >No BID detected")
            bid = 0
            bidSize = 0
        else:
            bid = self.msg['marketData']['BI'][0]['price']
            bidSize = self.msg['marketData']['BI'][0]['size']

        if not self.offerMsg:
            # >No OFFER detected")
            offer = 0
            offerSize = 0
        else:
            offer = self.msg['marketData']['OF'][0]['price']
            offerSize = self.msg['marketData']['OF'][0]['size']

            # print("Object MD() cRofexMessage created")
            # print("En cRofexMessage ", self.msg)


    def processMessage(self):

        print("Process msg OK")
        #self.md.append([self.msgType,self.timestamp, self.marketId,self.sym, self.bid, self.offer, self.bidSize, self.offerSize, self.id])

    def printMessage(self):
        #print ("Print Method: ",self.type,self.timestamp, self.marketId,self.sym, self.bid, self.offer, self.bidSize, self.offerSize, self.id)
        print ("Print method Array: ",self.md)

    def getLastMessage(self):
        return (self.msg)
        #print("Last Message :",self.md[-1])
        #print ("Last Message :",self.msg)