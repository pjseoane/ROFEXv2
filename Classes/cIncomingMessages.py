
class cIncomingMessages():
    def __init__ (self,msg):
        self.msg=msg

        self.md = []
        self.processMessage()


    def processMessage(self):

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

        self.md.append([self.timestamp, self.sym, self.bid, self.offer, self.bidSize, self.offerSize, self.numMessages])
        # print("MD Array :",self.md[-1])
        # return