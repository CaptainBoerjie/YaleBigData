import requests
import re
from readability import Document

response = requests.get(' http://www.omannews.gov.om/ona_n/description.jsp?newsId=277437')
raw_html=Document(response.text).summary()

cleanr = re.compile('<.*?>')
cleantext = re.sub(cleanr, '', raw_html)
stopterms = ['&#13;','13#&','&#13','\n','\xa0']
querywords = cleantext.split()
resultwords  = [word for word in querywords if word.lower() not in stopterms]
clean = ' '.join(resultwords)


print(clean)
