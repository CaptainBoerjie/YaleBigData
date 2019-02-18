from newspaper import Article

def test_newspaper(url):
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

if __name__ == "__main__":
    url = 'http://wam.ae/ar/details/1395302739836'
    test_newspaper(url)