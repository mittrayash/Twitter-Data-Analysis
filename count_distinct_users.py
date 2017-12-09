__author__ = 'mittr'
import pymongo

client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets


distinct_users = set()

for tweet in coll.find():
    distinct_users.add(tweet['user_id'])

print("{} distinct nodes our of {} total nodes".format(len(distinct_users), coll.count()))

