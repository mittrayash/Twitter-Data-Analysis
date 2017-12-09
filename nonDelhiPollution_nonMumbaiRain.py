__author__ = 'mittr'

import pymongo

client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets
new_db = db.outliers

count1 = 0
count2 = 0
for tweet in coll.find():
    if 'Delhi' not in tweet['location'] and 'pollution' in tweet['hashtags']:
        count1 += 1
    if 'Mumbai' not in tweet['location'] and ('rain' in tweet['hashtags'] or 'Ockhi' in tweet['hashtags']):
        count2 += 1

dict = {'tag': "non Delhi people who are discussing the issue of pollution", 'val': count1}
dict2 = {'tag':"non Mumbai people are discussing the issue of rains", 'val': count2}
new_db.insert(dict)
new_db.insert(dict2)
