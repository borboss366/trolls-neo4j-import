import urllib
from bs4 import BeautifulSoup
import csv
import requests

# testing for new version

url = "http://web.archive.org/web/20150603004258/https://twitter.com/AlwaysHungryBae"
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')

tweets = soup.find_all('li', attrs={'data-item-type': 'tweet'})

for t in tweets:
    tweet_obj = {}
    tweet_obj['tweet_id'] = t.get("data-item-id")
    tweet_container = t.find('div', attrs={'class': 'tweet'})
    tweet_obj['screen_name'] = tweet_container.get('data-screen-name')
    tweet_obj['permalink'] = tweet_container.get('data-permalink-path')
    tweet_content = tweet_container.find('p', attrs={'class': 'tweet-text'})
    tweet_obj['tweet_text'] = tweet_content.text
    tweet_obj['user_id'] = tweet_container.get('data-user-id')

    tweet_time = tweet_container.find('span', attrs={'class': '_timestamp'})
    tweet_obj['timestamp'] = tweet_time.get('data-time-ms')

    hashtags = tweet_container.find_all('a', attrs={'class': 'twitter-hashtag'})
    tweet_obj['hashtags'] = []
    tweet_obj['links'] = []

    for ht in hashtags:
        ht_obj = {}
        ht_obj['tag'] = ht.find('b').text
        ht_obj['archived_url'] = ht.get('href')
        tweet_obj['hashtags'].append(ht_obj)

    links = tweet_container.find_all('a', attrs={'class': 'twitter-timeline-link'})
    for li in links:
        li_obj = {}
        if li.get('data-expanded-url'):
            li_obj['url'] = li.get('data-expanded-url')
        elif li.get('data-resolved-url-large'):
            li_obj['url'] = li.get('data-resolved-url-large')
        else:
            li_obj['url'] = li.text
        li_obj['archived_url'] = li.get('href')
        tweet_obj['links'].append(li_obj)

    print(tweet_obj)