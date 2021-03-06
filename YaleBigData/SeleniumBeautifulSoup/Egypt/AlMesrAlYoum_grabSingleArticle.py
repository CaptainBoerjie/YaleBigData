# Egypt - Al Masr Al Youm
# https://www.almasryalyoum.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('h1', attrs={'class': 'tit_2'})
    date_box = soup.find('div', attrs={'class': 'pinfo'}).find('span')
    article_box_group = soup.find('div', attrs={'id': 'NewsStory'}).find_all('p')

    try:
        title = title_box.text.strip()
        date = date_box.text.strip()
        article = ''
        for p in article_box_group:
            article += p.text.strip()

        return [title,date,article]

    except AttributeError as e:
        return([None,None,None])
    
if __name__ == "__main__":

    page = 'https://almadapaper.net/Details/216314/'

    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])