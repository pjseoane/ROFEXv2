import threading
import queue
#from queue import Queue
import time


MAXQ=10
q = queue.Queue(MAXQ)
#q.put(111)
print_lock = threading.Lock()

def exampleJob(element):
   # time.sleep(.5)  # pretend to do some work.
    with print_lock:
        print("Threading name ->:", threading.current_thread().name, "  >Elemento Retirado->", element,"Qsize:",q.qsize())


# LLena una unica cola q con elementos a un ritmo del parametro timePause
def encolar(timePauseEnc):
    while q.qsize()<MAXQ:
    #while True:
        time.sleep(timePauseEnc)
        print("Add element to q, Qsize---->", q.qsize())

        q.put(time.perf_counter())

    print("Se alcanzo el limite de cola: --> ", MAXQ)


#Vacia la cola
def decolar(timePauseDec):
    while True:
    #while not q.empty():
        time.sleep(timePauseDec)

        element = q.get()
        # Run the example job with the avail worker in queue (thread)
        exampleJob(element)

        # completed with the job
        q.task_done()


def main():

        print("Hello Q")
        print("Threads Vivos: ",threading.active_count())
        print("Enumerate: ",threading.enumerate())

        #thread de encolado 1 / seg
        enc = threading.Thread(target=encolar,name="Encolar",args=(1,),daemon=True)
        enc.start()

        print("-----QSize:", q.qsize())
        start = time.time()
        print("Start Time: ", start)


        #threads de decolado sacan 1/ 3 seg
        for i in range (2):
            t= threading.Thread(target=decolar,args=(3,))
            #dec.setName("Decolar")
            t.daemon=True
            time.sleep(2)
            t.start()

        q.join()
        print("Total Time :",time.time()-start)
        print("Threads Vivos: ", threading.active_count())
        print("Enumerate: ", threading.enumerate())
        return

if __name__ == '__main__':
    main()
