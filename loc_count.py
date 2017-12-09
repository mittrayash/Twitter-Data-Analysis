__author__ = 'mittr'

import json, urllib, pymongo, requests
KEY = "AIzaSyDQu5R91stbmDaJ0HyWKF_EzbEJILsn_tw"  # Google Places API Key

MONGODB_URI = 'mongodb://localhost:27017/delhi_mumbai'
client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets
new_db = db.loc_count


def get_location(search_text): # Finds the city.
    try:
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        key = '?key=' + KEY
        query = '&query=' + urllib.parse.quote(search_text)
        url = url + key + query
        response = json.loads(requests.get(url).text)
        addr = response["results"][0]["formatted_address"]
        city = addr.split(", ")[0]
        country = addr.split(", ")[2]
        if country != "India":
            raise IndexError
    except IndexError:
        city = "India"
    return city  # If city cannot be found / city not given (most common case), city set to India

i = 0
location_count = {}
for tweet in coll.find():
    i += 1
    loc = get_location(tweet["location"])  # Creation of collection.
    if loc not in location_count:
        location_count[loc] = 1
    else:
        location_count[loc] += 1
    #if i%10 == 0:
    print(str(i) + " of 20000 done")  # to keep track of progress.

for x in location_count:
    jsonx = {"city": x, "tweets": str(location_count[x])}
    new_db.insert(jsonx)
