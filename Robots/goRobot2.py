import sys



global path
#path= 'C:/Users/pauli/'
path= 'C:Users/pseoane'

sys.path.append(path+'Documents/Python Projects/ROFEXv2/Classes/')
#sys.path.append('C:/Users/pauli/Documents/Python Projects/ROFEX/Classes')
#sys.path.append('C:/Users/pseoane/Documents/Python Projects/ROFEXv2/Classes')
from Classes import cSetUpEntorno as env
from Classes import cSuscript as sus

user1=env.cROFEXSetUp()
print(user1.instrumentos())
user1.newSingleOrder("ROFX","DoDic19","56.90","10","LIMIT","SELL","DAY",user1.account,"TRUE")
print("New Single order OK")
user1.consultarOrdenesActivas(user1.account)
user1.consultarOrdenesAllClientOrder(user1.account)

ticker1="DOMar19"
ticker2="RFX20Mar19"
suscriptArray=[ticker1,ticker2]
rob1=sus.cSuscription(user1,suscriptArray)