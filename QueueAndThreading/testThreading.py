import threading
import time
from datetime import datetime


def func(i):
    print("Tread #",i,"seconds",str(datetime.today().second))
    time.sleep(i*30)


for i in range(5):
    w = threading.Thread(target=func,args=(i,)).start()


def f(i):
    time.sleep(i*1000)
    return


t1 = threading.Thread(target=f, args=(1.2,), name="Thread#1")
t1.start()
t2 = threading.Thread(target=f, args=(2.2,), name="Thread#2")
t2.start()


for p in range(5):
    time.sleep(p*0.5)
    print('[',time.ctime(),']', t1.getName(), t1.is_alive())
    print('[',time.ctime(),']', t2.getName(), t2.is_alive())