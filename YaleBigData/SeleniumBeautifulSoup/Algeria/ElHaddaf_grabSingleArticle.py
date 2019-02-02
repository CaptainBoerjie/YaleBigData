# Algeria - El Khabar
# https://www.elkhabar.com 

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grab(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")

    title_box = soup.find('div', attrs={'class': 'right_area'}).find('h1')
    date_box = soup.find('div', attrs={'class': 'post_bare'}).find('span', attrs={'class': 'time'})
    article_box = soup.find('div', attrs={'id': 'post_core'}).find_all('p')

    title = title_box.text.strip()
    date = date_box
    article = ''
    for a in article_box:
        article += a.text.strip()

    print(title)
    print(date)
    #print(article)

if __name__ == "__main__":
    
    url = 'http://www.elheddaf.com/article/detail?id=633'
    grab(url)