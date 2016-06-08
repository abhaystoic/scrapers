'''
15 processes takes around 3-4 GB of RAM
'''
from subprocess import Popen
import time

processes = []
total_pages = (5289/50) + 1
num_of_processes = 10
start_pages = []
end_pages = []
page_dists = []
for j in xrange(0, num_of_processes):
    if j == 0:
        start_pages.append(1)
    else:
        start_pages.append(end_pages[j-1])
    if j < (num_of_processes - 1):
        end_pages.append((total_pages / num_of_processes) * (j + 1))
        page_dists.append((start_pages[j], end_pages[j]))
    else:
        page_dists.append((start_pages[j], total_pages + 1))
print page_dists
for i in xrange(0, num_of_processes):
    #print page_dists[i][0], page_dists[i][1]
    processes.append(Popen('C:\Python27\python.exe scraper6.py {} {}'.format(page_dists[i][0], page_dists[i][1]), shell=True))
    
start_time = time.time()
for process in processes:
    process.wait()
print "FINAL PROCESSING TIME =", str((time.time() - start_time)/60), 'minutes'