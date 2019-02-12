import feedparser
import Newspaper_singlearticle


feed = feedparser.parse('https://alwafd.news/feed/26')

print(feed.entries[0].title)
print(feed.entries[0].link)
try:
    print(feed.entries[0].published)
except:
    print("NO RSS FEED DATE")

try:
    Newspaper_singlearticle.test_newspaper(feed.entries[0].link)
except:
    print("NEWSPAPER FAILED")