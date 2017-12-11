__author__ = 'mittr'
import pymongo


client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets
nodes = []
reply_edges = []
mention_edges = []
retweet_edges = []

for x in coll.find():  # get reply, mentions, and retweet edges
    nodes.append({"name": x["user"],"user_id": x["user_id"]})

    if x['inReplyTo'] is not None:
        reply_edges.append({"user_id": x["user_id"], "inReplyTo": x["inReplyTo"]})

    if len(x['mentions']) > 0:
        mntn = [x['mentions'][i] for i in range(len(x['mentions']))]
        mention_edges.append({"user_id": x["user_id"], "mentions": mntn})
    if x['Retweet']:
        retweet_edges.append({'retweeter': x["user_id"], "retweeted": x["retweetedFrom"]})

file = open('data.json', 'a', encoding="utf-8")
file.write('{"nodes":[')
for i in range(len(nodes)):
    file.write((str(nodes[i])))
    if i < len(nodes)-1:
        file.write(',')
    else:
        file.write('],"links":[')

for i in range(len(retweet_edges)):
    file.write(str(retweet_edges[i]))
    if i < len(retweet_edges)-1:
        file.write(',')
    else:
        file.write(']}')
