

import csv
import pymysql
import datetimehandler
import os
from datetime import datetime
from requests import exceptions as reqEx
from selenium.common import exceptions as selEx
import threading

def grabarticle(country,source,link,min,max):


grablist = []
with open('HistoricGrabList.csv','r') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        grablist.append(row)

for i in grablist:
    t = threading.Thread(target=grabarticle,args=(i[0],i[1],i[2],i[3],i[4],))
    