__author__ = 'mittr'
import pymongo

client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets
nodes = []
for x in coll.find():  # get reply, mentions, and retweet edges
    nodes.append({"user_id": x["user_id"]})
print(nodes)