import threading
from queue import Queue
import time
# ver esta web
#https://docs.python.org/3/library/queue.html

#variable para lockear un thread
print_lock = threading.Lock()
#worker deberian ser el bot / symbols o grupo de symmbols

def exampleJob(worker):
    time.sleep(.5) # pretend to do some work.
    with print_lock:
        print("Threading name ->:",threading.current_thread().name,"  Worker ->",worker)


# Create the queue and threader
#Aloja los workers / bots
q = Queue()


# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()
        print("Get a worker",q.qsize())
        # Run the example job with the avail worker in queue (thread)
        exampleJob(worker)

        # completed with the job
        q.task_done()



def main():
    # how many threads are we going to allow for
    # 1 thread por symbols/contract
    for x in range(10):
        t = threading.Thread(target=threader)

        # classifying as a daemon, so they will die when the main dies
        t.daemon = True

        # begins, must come after daemon definition
        t.start()

    start = time.time()

    # 20 jobs assigned.
    for worker in range(20):
        print("Add a worker to q", q.qsize())
        q.put(worker)

    # wait until the thread terminates.
    q.join()

    # with 10 workers and 20 tasks, with each task being .5 seconds, then the completed job
    # is ~1 second using threading. Normally 20 tasks with .5 seconds each would take 10 seconds.
    print('Entire job took:',time.time() - start)
    #los threads permanecen abiertos ??
if __name__ == '__main__':
    main()