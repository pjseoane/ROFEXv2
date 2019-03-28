import sys


global path
#path= 'C:/Users/pauli/'
path= 'C:Users/pseoane'

sys.path.append(path+'Documents/Python Projects/ROFEXv2')

import Classes.cSetUpEntorno as env
import Classes.cSuscript as sus
#from Classes import cSetUpEntorno as env
#from Classes import cSuscript as sus

user1=env.cROFEXSetUp()
print(user1.instrumentos())
user1.newSingleOrder("ROFX","DoDic19","56.90","10","LIMIT","SELL","DAY",user1.account,"TRUE")
print("New Single order OK")
user1.consultarOrdenesActivas(user1.account)
print (user1)
user1.consultarOrdenesAllClientOrder(user1.account)
print(user1)

ticker1="DOMar19"
ticker2="RFX20Mar19"
ticker3="DOJun19"
ticker4="RFX20Jun19"
suscriptArray=[ticker1,ticker2]
suscripArray2=[ticker3,ticker4]
rob1=sus.cSuscription(user1,suscriptArray)
rob2=sus.cSuscription(user1,suscripArray2)

# Arquitectura
# user = rofex.Setup()
# algo1 = suscribir (user, arraysTickers)
# ..........ticker1 o ticker[0].bid  .msg


