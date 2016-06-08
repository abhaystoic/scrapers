'''
Created on Jun 7, 2016

@author: abgupta
'''
import threading

def run_do_ping(addr):
   p = do_ping(addr)
   p.wait()

###

# start all threads
z = []
for i in range(0, len(IP_LIST)):
   t = threading.Thread(target=run_do_ping, args=(IP_LIST[i],))
   t.start()
   z.append(t)

# wait for all threads to finish
for t in z:
   t.join()