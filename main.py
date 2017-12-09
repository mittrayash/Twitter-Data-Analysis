__author__ = 'mittr'

from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

#MONGODB_URI = 'mongodb://localhost:27017/delhiPollution_mumbaiRains'
MONGODB_URI = 'mongodb://user:pass@ds133856.mlab.com:33856/delhi_mumbai'
mongo = PyMongo(app)

@app.route('/')
def index():
    client = MongoClient(MONGODB_URI)
    db = client['delhi_mumbai']
    all_tweets = db['all_tweets']
    total_count = all_tweets.count()
    return str(total_count)


if __name__ == '__main__':
    app.debug = True
    app.run()
delhiPollution_mumbaiRains
#app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/delhiPollution_mumbaiRains'
#mongo = PyMongo(app, config_prefix='MONGO')
