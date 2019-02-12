from multiprocessing import Pool
import os
import random

def service(x):
    s = 0
    for i in range(x):
        s = s * i
    print("Finished - ",os.getpid() )

p = Pool()
randlist = []
for i in range(20):
    randlist.append(random.randrange(1000))

p.map(service, randlist)
p.close()
p.join()
