from bs4 import BeautifulSoup
import requests
import json

tweet_arr = []
with open('available_urls.csv') as f:
    #with open('tweets_2.csv', 'w') as tweet_file:
    #    writer  = csv.writer(tweet_file)
    for l in f:
        page = requests.get(l).text
        soup = BeautifulSoup(page, 'html.parser')
        
        tweets = soup.find_all('div', attrs={'data-item-type': 'tweet'})
        for t in tweets:
            tweet_container = t.find('div')
            try:
                tweet_content = tweet_container.find('p', attrs={'class': 'ProfileTweet-text'}).text
                tweet_obj = {}
                tweet_obj['tweet_text'] = tweet_content
                tweet_obj['permalink'] = tweet_container.find('a', attrs={'class': 'js-permalink'}).get('href')
                tweet_obj['screen_name'] = tweet_container.get('data-screen-name')
                tweet_obj['tweet_id'] = tweet_container.get('data-tweet-id')
                tweet_obj['user_id'] = tweet_container.get('data-user-id')
                tweet_obj['links'] = []
                tweet_obj['hashtags'] = []
                print("--------------------")
                for l in tweet_container.find_all('a', attrs={'class': 'twitter-timeline-link'}):
                    lo = {}
                    lo['archived_url'] = l.get('href')
                    lo['url'] = l.text
                    tweet_obj['links'].append(lo)
                for h in tweet_container.find_all('a', attrs={'class': 'twitter-hashtag'}):
                    ht = {}
                    ht['tag'] = h.find('b').text
                    ht['archived_url'] = h.get('href')
                    tweet_obj['hashtags'].append(ht)
                print("--------------------")
                tweet_arr.append(tweet_obj)
                print("processed a user")
            except:
                pass

        if not tweets:
            #newer html version
            tweets = soup.find_all('li', attrs={'data-item-type': 'tweet'})
            try:
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

                    print("--------------------")
                    tweet_arr.append(tweet_obj)
                    print("processed a user")

            except:
                pass
        if not tweets:
            print("NO TWEETS FOR " + l)                

with open('tweets_full.json', 'w') as f:
    json.dump(tweet_arr, f, ensure_ascii=False, sort_keys=True, indent=4)
