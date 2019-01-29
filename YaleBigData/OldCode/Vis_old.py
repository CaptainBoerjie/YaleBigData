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