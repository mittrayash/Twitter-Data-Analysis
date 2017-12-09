__author__ = 'mittr'

from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import render_template

app = Flask(__name__)

MONGODB_URI = 'mongodb://localhost:27017/delhi_mumbai'
#MONGODB_URI = 'mongodb://user:pass@ds133856.mlab.com:33856/delhi_mumbai'
mongo = PyMongo(app)

client = MongoClient(MONGODB_URI)
db = client['delhi_mumbai']
all_tweets = db['all_tweets']
# Calling all collections

app = Flask(__name__)
@app.route('/')
def main():
    nodes = []
    reply_edges = []
    mention_edges = []
    retweet_edges = []
    count1 = 0
    for x in all_tweets.find():
        nodes.append({"user_id": x["user_id"], "hashtags": x["hashtags"]})  # Initialising those templates.

        if x['inReplyTo'] is not None:
            reply_edges.append({"user_id": x["user_id"], "inReplyTo": x["inReplyTo"]})

        if len(x['mentions']) > 0:
            mntn = [x['mentions'][i] for i in range(len(x['mentions']))]
            mention_edges.append({"user_id": x["user_id"], "mentions": mntn})
        if x['Retweet']:
            retweet_edges.append({"retweeter": x["user_id"], "retweeted": x["retweetedFrom"]})

    return render_template('index.html', nodes=nodes, reply_edges=reply_edges, mention_edges=mention_edges, retweet_edges=retweet_edges)


if __name__ == '__main__':
    app.debug = True
    app.run()

