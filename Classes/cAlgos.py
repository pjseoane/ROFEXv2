import threading

class cRobot():
    def __init__(self, contract1,contract2):

        self.c1=contract1
        self.c2=contract2

        #self.goRobot()
       # threading.Thread(target=self.goRobot,daemon=True).start()

    def goRobot(self):
        while True:
            print ("En Algos")
            print (self.c1.md[-1]," mensajes>>>>>:", len(self.c1.md))
            print (self.c2.md[-1],"mensajes>>>>>>:", len(self.c2.md))



        #return



