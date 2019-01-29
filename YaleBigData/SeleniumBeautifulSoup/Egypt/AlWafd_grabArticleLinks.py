# Egypt - Al Wafd
# http://alwafd.news

# This code uses Selenium and BeautifulSoup to get all the news article
# links for a given category page (target_url).
# Selenium clicks on the 'load more' button at the bottom of the page
# then regrabs the page source before passing it to BeautifulSoup

# works really well, last run, found 3597 links

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

opts = Options()
opts.set_headless()

assert opts.set_headless
browser = Firefox(options=opts)
target_url = 'https://alwafd.news/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%D8%AA%D9%82%D8%A7%D8%B1%D9%8A%D8%B1'
browser.get(target_url)

while True:
    try:
        browser.find_element_by_xpath('//*[@id="end"]').click()
        time.sleep(5)
    except NoSuchElementException:
        break

page = browser.page_source
soup = BeautifulSoup(page, 'lxml')

main_container = soup.find('div', attrs={'id': 'infinite'})

link_cnt = 0
for a in main_container.find_all('div', "item tile-boost"):
    link_cnt += 1
    print(a.find('a')["href"])

print("Total links: ", link_cnt)