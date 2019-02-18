# Oman - Oman Official News Agency
# https://omannews.gov.om

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

from bs4 import BeautifulSoup
import requests

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('blockquote', attrs={'class': 'bbg'}).find('p')
    #date_box = soup.find('div', attrs={'id': 'bg'}).find('div', attrs={'class': 'col-md-12'}).find('b')
    article_box = soup.soup.find('div', attrs={'class': 'tab-content'}).find_all('p')

    try:
        title = title_box.text.strip()
        date = None #date_box.text.strip()
        article = ''
        for a in article:
            a += article.text.strip()
            
        return [title,date,article]
    except AttributeError as e:
        return([None,None,None])

if __name__ == "__main__":

    page = 'https://omannews.gov.om/ona_n/description.jsp?newsid=277437'
    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])

