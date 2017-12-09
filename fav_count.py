__author__ = 'mittr'
import pymongo

client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets
new_db = db.fav_count

fav_count = {100:0,90:0,80:0,70:0,60:0,50:0,40:0,30:0,20:0,10:0,0:0}  # Fav counts greater than dict key will be added.
for tweet in coll.find():
    md = tweet["Fav"]
    for i in fav_count:
        if md >= i:
            fav_count[i] += 1
            break

print(fav_count)
for x in fav_count:
    jsonx = {"favs": x, "count": fav_count[x]}
    new_db.insert(jsonx)