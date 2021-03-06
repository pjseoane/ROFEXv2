from itertools import count #itertools es para contar la cantidad de instancias de una clase
import simplejson

class cRofexMessage():

    _ids = count(0)
    md = []

    def __init__ (self, message):

        self.bid = 0
        self.offer = 0
        self.bidSize = 0
        self.offerSize = 0
        self.numMessages = 0
        self.timestamp = 0
        self.indexBid = 0
        self.indexOffer = 0
        self.sym = ""
        self.marketId= ""

        self.id = next(self._ids)  # se cuenta la cantidad de instancias de una clase

        self.msg = simplejson.loads(message)
        msgType = self.msg['type'].upper()

        if msgType == 'MD':
            self.incomingMD()
            self.processMessage()

        elif msgType == 'OR':
            print("En Mensaje OR")
            print(self.msg)
        else:
            print("Tipo de Mensaje Recibido No soportado: " + self.msg)


    def incomingMD(self):

        self.timestamp = self.msg['timestamp']
        self.marketId = self.msg['instrumentId']['marketId']
        self.sym = self.msg['instrumentId']['symbol']
        # Aca hay un problema si no hay bid u offer pq solo viene ['marketData']
        bidMsg = self.msg['marketData']['BI']
        offerMsg = self.msg['marketData']['OF']

        if bidMsg:

            self.bid = self.msg['marketData']['BI'][0]['price']
            self.bidSize = self.msg['marketData']['BI'][0]['size']

        if offerMsg:

            self.offer = self.msg['marketData']['OF'][0]['price']
            self.offerSize = self.msg['marketData']['OF'][0]['size']

        # print("Object MD() cRofexMessage created")
        # print("En cRofexMessage ", self.msg)
        self.md.append(self.getLastMessage())
        print("Len md en cRofexMessage:", len(self.md))

    def getBid(self):
        return (self.bid)

    def getBidSize(self):
        return (self.bidSize)

    def getOffer(self):
        return (self.offer)

    def getOfferSize(self):
        return (self.offerSize)


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