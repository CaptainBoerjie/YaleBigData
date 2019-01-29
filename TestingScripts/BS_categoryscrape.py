# This code outputs all the article links from Al Wafd on the main news page

from bs4 import BeautifulSoup
import requests

category_url = 'https://alwafd.news/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%D8%AA%D9%82%D8%A7%D8%B1%D9%8A%D8%B1'

page = requests.get(category_url)
soup = BeautifulSoup(page.content, 'html.parser')

main_container = soup.find('div', attrs={'id': 'infinite'})

link_cnt = 0
for a in main_container.find_all('div', "item tile-boost"):
    link_cnt += 1
    print(a.find('a')["href"])

print("Total links: ", link_cnt)