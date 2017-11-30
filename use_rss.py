import feedparser
from pprint import pprint

rss_url = "https://www.leiphone.com/feed"
data = feedparser.parse(rss_url)

pprint(data.entries[0])
