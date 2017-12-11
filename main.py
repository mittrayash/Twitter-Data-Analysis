__author__ = 'mittr'

from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import Flask, render_template


# MONGODB_URI = 'mongodb://localhost:27017/delhi_mumbai'
MONGODB_URI = 'mongodb://user:pass@ds133856.mlab.com:33856/delhi_mumbai'
# DB_URI Changed to remote one after uploading the files there
client = MongoClient(MONGODB_URI)
db = client['delhi_mumbai']
all_tweets = db['all_tweets']
fav_count = db['fav_count']
hash_count = db['hash_count']
tweet_type_count = db['tweet_type_count']
type_count = db['type_count']
loc = db.loc_count
outliers = db.outliers

app = Flask(__name__)
@app.route('/')
def main():
    nodes = []
    reply_edges = []
    mention_edges = []
    retweet_edges = []
    favorite_count = []
    media_count=[]
    orig_retweets = []
    hashtag_count = []
    location_count = []
    outliers_count = []

    for x in outliers.find():
        outliers_count.append({"tag": x['tag'], "value": x["val"]})


    for x in loc.find():
        location_count.append({"city":x["city"], "tweets":x["tweets"]})

    for x in fav_count.find():
        favorite_count.append({"favs":str(x["favs"]), "count":x["count"]})

    for x in type_count.find():
        media_count.append(x["hits"])

    for x in tweet_type_count.find():
        orig_retweets.append(x["Distribution"])

    i = 1
    for x in hash_count.find():
        hashtag_count.append({"index":i, "hashtag":x["hashtag"], "count":x["count"]})
        i += 1

    return render_template('index.html', outliers_count=outliers_count, location_count=location_count, nodes=nodes, reply_edges=reply_edges, mention_edges=mention_edges, retweet_edges=retweet_edges, orig_retweets=orig_retweets, hashtag_count=hashtag_count, media_count=media_count, favorite_count=favorite_count)


if __name__ == '__main__':
    app.debug = True
    app.run()


