# Libya - Akhbar Libya
# https://www.akbarlibya.net

# This code requires Selenium because the html is generated by javascript and so
# BS alone is unable to find <html> tags in the source because none have been generated

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('h1', attrs={'class': 'post-title'})
    date_box = soup.find('time', attrs={'class': 'post-date'}).get('datetime')
    article_box = soup.find('section', attrs={'class','article-content'}).find('div')

    try:
        title = title_box.text.strip()
        date = date_box
        print(date)
        
        article = ''
        for a in article_box:
            print(a)
            article += a.text.strip()

        return [title,date,article]

    except AttributeError as e:
        return([None,None,None])

if __name__ == "__main__":

    page = 'http://www.akhbarlibya.net/arabic-news/10000.html'

    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])