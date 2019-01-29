from newspaper import Article

def test_newspaper(url):
    url = 'http://elkhabar.com/press/article/149351/%D8%A7%D9%84%D8%B4%D8%B1%D8%B7%D8%A9-%D8%A7%D9%84%D8%A8%D8%B1%D9%8A%D8%B7%D8%A7%D9%86%D9%8A%D8%A9-%D8%AA%D8%AD%D8%B0%D8%B1-%D8%A7%D9%84%D8%A3%D9%85%D9%8A%D8%B1-%D9%81%D9%8A%D9%84%D9%8A%D8%A8'
    toi_article = Article(url, language='ar')
    toi_article.download()
    toi_article.parse()

    #To extract title 
    print("Article's Title:") 
    print(toi_article.title) 
    print("\n") 

    #To extract title 
    print("Article's Date:") 
    print(toi_article.publish_date) 
    print("\n") 

    #To extract text 
    print("Article's Text:") 
    print(toi_article.text) 
    print("\n") 
    
    #To extract summary 
    #print("Article's Summary:") 
    #print(toi_article.summary) 

    
    #To extract keywords 
    #print("Article's Keywords:") 
    #print(toi_article.keywords) 