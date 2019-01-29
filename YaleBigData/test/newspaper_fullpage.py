import newspaper

news = newspaper.build('https://www.elkhabar.com')

for category in news.category_urls():
    print(category)
    subnews = newspaper.build(category)
    for article in subnews.articles:
        print(article.url)


