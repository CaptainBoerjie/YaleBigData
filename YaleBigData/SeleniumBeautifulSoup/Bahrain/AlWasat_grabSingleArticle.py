# Bahrain - Al Wasat News
# https://www.alwasatnews.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article


from bs4 import BeautifulSoup
import requests

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    try:
        title_box = soup.find('div', attrs={'class': 'c-main'}).find('h1')
        date_box = soup.find('p', attrs={'class': 'time rs_skip'}).find('span').get('title')
        article_box = soup.find('span', attrs={'class': 'news_content'}).find_all('p')
    
        article = ''
        for a in article_box:
            article += a.text
        title = title_box.text.strip()
        date = date_box
        return [title,date,article]

    except AttributeError as e:
        return([None,None,None])

if __name__ == "__main__":

    page = 'http://www.alwasatnews.com/news/1247105.html'
    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])