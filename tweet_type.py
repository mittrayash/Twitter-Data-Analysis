__author__ = 'mittr'

import pymongo

client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets
new_db = db.tweet_type_count

tweet_type = {'original': 0, 'retweets': 0}

for tweet in coll.find():
    if tweet['Retweet'] == True:
        tweet_type['original'] += 1
    else:
        tweet_type['retweets'] += 1

json = {"category": "Original Tweets", "Distribution": tweet_type['original']}
new_db.insert(json)
json = {"category": "Retweets", "Distribution": tweet_type['retweets']}
new_db.insert(json)
