from itertools import count #itertools es para contar la cantidad de instancias de una clase
import simplejson

class cRofexMessage():
    _ids = count(0)

    def __init__ (self,message):

        self.id = next(self._ids)  # se cuenta la cantidad de instancias de una clase
        #self.msg=msg
        self.msg = simplejson.loads(message)
        self.md = []
        print("Object cRofex Message created")
        print(self.msg)
        self.processMessage()


    def processMessage(self):

        self.type       = self.msg['type'].upper()
        self.timestamp  = self.msg['timestamp']
        self.marketId   = self.msg['marketId']
        self.sym        = self.msg['instrumentId']['symbol']
        print("Process msg OK")
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



        self.md.append([self.type,self.timestamp, self.marketId,self.sym, self.bid, self.offer, self.bidSize, self.offerSize, self.id])
        # print("MD Array :",self.md[-1])
        # return


    def printMessage(self):
        print (self.type,self.timestamp, self.marketId,self.sym, self.bid, self.offer, self.bidSize, self.offerSize, self.id)