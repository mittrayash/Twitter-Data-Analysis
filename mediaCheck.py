__author__ = 'mittr'
import pymongo

client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets
new_db = db.type_count

type_count = {"text": 0, "image":0, "both":0}
for tweet in coll.find():
    md = tweet["media"]
    if len(md) != 0:
        if tweet["content"] == "":
            type_count["image"] += 1 # Only Image
        else:
            type_count["both"] += 1 # Image and text
    else:
        type_count["text"] += 1 # Only text

jsonx = {"category": "text", "hits": str(type_count["text"])}
new_db.insert(jsonx)
jsonx = {"category": "image", "hits": str(type_count["image"])}
new_db.insert(jsonx)
jsonx = {"category": "both", "hits": str(type_count["both"])}
new_db.insert(jsonx)