---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

ax = plt.axes(projection=ccrs.Mollweide())
ax.stock_img()
plt.show()

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()

ny_lon, ny_lat = -75, 43
delhi_lon, delhi_lat = 77.23, 28.61

plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
         color='blue', linewidth=2, marker='o',
         transform=ccrs.Geodetic(),
         )

plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
         color='gray', linestyle='--',
         transform=ccrs.PlateCarree(),
         )

plt.text(ny_lon - 3, ny_lat - 12, 'New York',
         horizontalalignment='right',
         transform=ccrs.Geodetic())

plt.text(delhi_lon + 3, delhi_lat - 12, 'Delhi',
         horizontalalignment='left',
         transform=ccrs.Geodetic())

plt.show()

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

from mpl_toolkits import mplot3d

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()
ax = plt.axes(projection='3d')

ax = plt.axes(projection='3d')

# Data for a three-dimensional line
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')

# Data for three-dimensional scattered points
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

from mpl_toolkits import mplot3d

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()
ax = plt.axes(projection='3d')

# Data for three-dimensional scattered points

xdata = [1,2,3,4,5,6,7,8,9,10]
ydata = [2,4,6,8,10,2,14,16,18,20]
zdata = [1,2,3,4,20,6,7,8,9,10]
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pymysql
 
    
db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()
sql_selectQuery = """SELECT DISTINCT fee_country, COUNT(*) FROM
(SELECT DISTINCT fee_country, fee_source FROM feeds)
as custom GROUP BY fee_country;"""
cursor.execute(sql_selectQuery)
allFeeds = cursor.fetchall()

objects = []
performance = []
colors = []

populations = [42008000,1556000,99375000,39339000,9903000,4197000,6093000,6470000,\
          4540000,3619100,4829000,5052000,2694000,33554000,41511000,11659000,\
          9541000,28915000]
for pop in populations:
    color = "0x%0.6X" % (int((255*pop)/100000000))
    colors.append('#'+color[2:])

for row in allFeeds:
    objects.append(row[0])
    performance.append(row[1])

y_pos = np.arange(len(objects))
 
plt.bar(y_pos, performance, align='center', color=colors, alpha = 0.75)
plt.xticks(y_pos, objects, rotation='70')
plt.ylabel('Sources')
plt.title('News Sources by Country\n(Country population denoted by brightness)')
 
plt.show()
db.close()

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
objects = ('100', '200', '600', '1000', '2000', '3000')
y_pos = np.arange(len(objects))
performance = [64,64,63,61,58,54]
 
maxalpha = max(performance)+10
alphas = []
for i in range(len(performance)):
    newalpha = str(performance[i]/maxalpha)
    alphas.append(newalpha)

plt.bar(y_pos, performance, align='center', color=alphas, alpha=0.8)
plt.xticks(y_pos, objects)
plt.ylabel('Sentiment')
plt.title('Search Term: \"Donald Trump\"')
 
plt.show()

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
objects = ('100', '200', '600', '1000', '2000', '3000')
y_pos = np.arange(len(objects))
performance = [75,69,60,57,54,54]

maxalpha = max(performance)+10
alphas = []
for i in range(len(performance)):
    newalpha = str(performance[i]/maxalpha)
    alphas.append(newalpha)
 
plt.bar(y_pos, performance, align='center', color=alphas, alpha=0.9)
plt.xticks(y_pos, objects)
plt.ylabel('Sentiment')
plt.title('Search Term: \"Khashoggi\"')
 
plt.show()

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

# this code grabs a segment of text (segmentSize x 2 characters) with a search term in the middle
# then the code builds the Microsoft Azure POST json

import pymysql
import re
import requests
from pprint import pprint

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()

searchterm = '%خاشقجي%'
cursor.execute("SELECT news_id, news_text FROM news WHERE news_text LIKE %s LIMIT 400;",searchterm)
allresult = cursor.fetchall()

documents = []
idcount=[]
counter = 1

for result in allresult: 
    text = result[1]
    text = text[2000:]
    startindex = 0
    endindex = 0
    segmentSize = 200
    
    mcounter = 0
    for m in re.finditer(searchterm[1:(len(searchterm)-1)], text):

        if m.start() < segmentSize:
            startindex = 0
        else:
            startindex = m.start() - segmentSize
        if (m.end() + segmentSize) > len(text):
            endindex = len(text)
        else:
            endindex = m.end() + segmentSize
        document = {}
        document['id'] = str(counter)
        document['language']='ar'
        document['text']=text[startindex:endindex]
        documents.append(document)
        
        counter=counter+1
        idcount.append(result[0])

masterdic = {}
masterdic['documents'] = documents


# -----------------------------------------------------------

subscription_key = 'b8695a160e534e488f8c17082124397b'
assert subscription_key

text_analytics_base_url = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"

sentiment_api_url = text_analytics_base_url + "sentiment"

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(sentiment_api_url, headers=headers, json=masterdic)
sentiments = response.json()
pprint(sentiments)

# --------------------------------------------------------------

countryScores = {"Algeria":0,
                "Bahrain":0,
                "Egypt":0,
                "Iraq":0,
                "Jordan":0,
                "Kuwait":0,
                "Lebanon":0,
                "Libya":0,
                "Mauritania":0,
                "Morocco":0,
                "Oman":0,
                "Palestine":0,
                "Qatar":0,
                "Saudi Arabia":0,
                "Sudan":0,
                "Tunisia":0,
                "UAE":0,
                "Yemen":0}
scores = sentiments['documents']
cnt = 0
for score in scores:
    cursor.execute("SELECT news_country FROM news WHERE news_id=%s;",idcount[cnt])
    country=cursor.fetchone()
    cnt=cnt+1
    oldscore=countryScores[country[0]]
    countryScores[country[0]]=(oldscore + score['score'])/2
          
print(countryScores)

objects = ("Algeria",
                "Bahrain",
                "Egypt",
                "Iraq",
                "Jordan",
                "Kuwait",
                "Lebanon",
                "Libya",
                "Mauritania",
                "Morocco",
                "Oman",
                "Palestine",
                "Qatar",
                "Saudi Arabia",
                "Sudan",
                "Tunisia",
                "UAE",
                "Yemen")

sentiment=[]
for country in countryScores:
    sentiment.append(countryScores[country])
    
y_pos = np.arange(len(objects))

maxalpha = max(sentiment)+0.10
alphas = []
for i in range(len(sentiment)):
    newalpha = str(sentiment[i]/maxalpha)
    alphas.append(newalpha)

plt.bar(y_pos, sentiment, align='center', color=alphas, alpha=0.9)
plt.xticks(y_pos, objects,rotation=70)
plt.ylabel('Sentiment')
plt.title('Search Term: \"Jamal Khashoggi\"\n(Sentiment by country)')
 
plt.show()
          
db.close()