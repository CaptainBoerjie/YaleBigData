import newspaper

news = newspaper.build('https://www.elkhabar.com/press/category/28/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%84%D9%88%D8%B7%D9%86/')

for article in news.articles:
    print(article.url)
    article.download()
    article.parse()
    print(article.text)