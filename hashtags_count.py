__author__ = 'mittr'
# Queries the all_tweets collection and creates a new collection with the occurrences of the 10 most common hashtags.
import pymongo

client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets
new_db = db.hash_count

hashtag_count = {}
for tweet in coll.find():
    ht = tweet["hashtags"]
    for hash in ht:
        hash = hash.lower()
        if hash not in hashtag_count:
            hashtag_count[hash] = 1
        else:
            hashtag_count[hash] += 1

hc = sorted(hashtag_count, key=hashtag_count.get, reverse=True)  # Sorting the top 10.
count = 0

for z in hc:
    if count == 10:
        break
    jsonx = {"hashtag": z, "count": str(hashtag_count[z])}
    new_db.insert(jsonx)
    count += 1