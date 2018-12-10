import threading
import sys
#sys.path.append('C:/Users/pauli/Documents/Python Projects/ROFEX/Classes')
sys.path.append('C:/Users/pseoane/Documents/Python Projects/ROFEXv2/Classes')
from Classes import cSetUpEntorno as env
from Classes import cSuscriptV2 as sus
from Classes import cAlgos as bot


"""
def pintToScreen():
    while True:
        print("En goRobot***->", len(self.md), self.numMessages, "--", self.sym, "-->", self.bid, "/", self.offer,
              "    ", self.bidSize, "/", self.offerSize)
"""

def main():
    user1=env.cROFEXSetUp()
    x1=sus.cSuscription(user1,["DODic18"])
    x2=sus.cSuscription(user1,["RFX20Dic18"])

    bot1= bot.cRobot(x1,x2)
    goBot=threading.Thread(target=bot1.goRobot,name="goRobot",args=(),daemon=True)
    goBot.start()

if __name__ == '__main__':
    main()
