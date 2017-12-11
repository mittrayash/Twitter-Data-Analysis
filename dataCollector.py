import tweepy,pymongo

# Two keys needed - since rate limit 15k. IF rate limit hit, change key
# --------------------------------------------------------------------------------------------
''' SET 1 '''
conskeys = "dEj9PuikWT7amd5Ud5k79jurB"
consecret ="5nGkmWffNKIepE5bKjzj6RNLn0RTjjjLgxeVFp19ZLFwcOP40H"
acctok = "895015384507498496-drN0ZC4fAcKZWG0uk4g1ACQvILaUECZ"
acctoksecret = "rcpKoy7OnipvbnblpPwVamPVvJKoQGt5Ux88sUz1tn0Oj"

''' SET 2 '''
# conskeys = "p6tGekq0M3dPEkEWWxiv4DcmH"
# consecret ="jGqeSLD5wyU66iNUhlLOMtpNaaNeNXtAuKSJHyf09fUD4r75OJ"
# acctok = "938710222138470400-dzntQAZ2iHqeCSDs9lVX9WO3SWLcLsH"
# acctoksecret = "3wOdVSudgZPPnc0CfcRJNvPttkx7HtTjvwyvNsz0JFG

# Authentication
auth = tweepy.OAuthHandler(conskeys, consecret)
auth.set_access_token(acctok, acctoksecret)
api = tweepy.API(auth)
# ===============================================================================================
# Two queries - use one by one to curate 20,000 entries [10k each for Delhi Air Pollution and Mumbai Rain]
query = "#DelhiSmog OR #MyRightToBreathe OR #CropBurningDelhi OR #AirPollutionDelhi OR #LetMeBreatheDelhi OR #DelhiAirQuality OR #DelhiSmog OR #DelhiPollution OR #OddEven OR #OddEvenScheme OR #SaveDelhiAir OR #DelhiAir"
#query = "#MumbaiRains OR #mumbaiRainedout OR #bombayRains OR #CycloneOckhi OR #saveFisherMenMumbai OR #mumbaiFloods OR #bombayRain OR #rainingMumbai OR #mumbaiRain"
maxTweets = 10000  # Work this program twice for the two queries - go one by one and change to set 2 after 10k done
tpq = 100  # Tweets per query1
max_id = -1  # Setting a max_id to remove redundancy in case any of the queries raise an exception
count = 0

client = pymongo.MongoClient()
db = client.delhi_mumbai
coll = db.all_tweets  # Setting collection to enter documents.

while count < maxTweets:  # To keep the extraction running even if exception is raised.
    try:
        if max_id < 0:
            new_tweets = api.search(q=query, count=tpq, tweet_mode="extended") # For the first time
        else:
            new_tweets = api.search(q=query, count=tpq, max_id=str(max_id-1), tweet_mode="extended")
        if not new_tweets:
            print("END OF TWEETS")  # If we exhaust all the tweets.
            break
        for tweet in new_tweets:
            # Collecting data from the tweet JSON we require to process later
            id = tweet.id_str
            user_id = tweet.user.id_str
            user = tweet.user.name
            inReplyTo = tweet.in_reply_to_user_id
            try:
                x = tweet.retweeted_status  # Can't be accessed if not retweet.
                retweetedFrom = x.user.id_str
                RT = True
            except AttributeError:  # If original tweet
                retweetedFrom = -1
                RT = False
            if RT:
                content = tweet.retweeted_status.full_text
                fav = -1  # Fav count only in case of original tweets.
            else:
                content = tweet.full_text
                fav = tweet.favorite_count
            timestamp = str(tweet.created_at)
            location = tweet.user.location
            ht = tweet.entities["hashtags"]
            hashtags = []
            for i in ht:
                hashtags.append(i["text"]) # List of hashtags.
            mntn = tweet.entities["user_mentions"]
            mentions = []
            for i in mntn:
                mentions.append(i['id_str']) # List of mentions
            try:
                md = tweet.entities["media"]
                media = []
                for i in md:
                    media.append(i["url"]) # And list of media (photos only)
            except KeyError:  # If no media found
                media = []
            try:
                jsonx = {"_id": id, "user": user, "user_id": user_id, "content": content, "timestamp": timestamp, "location": location,
                         "hashtags": hashtags, "mentions": mentions, "inReplyTo": inReplyTo, "retweetedFrom": retweetedFrom, "media": media, "Retweet": RT, "Fav": fav} # Making a JSON to be sent to collection.
                coll.insert(jsonx)  # And insert
            except pymongo.errors.DuplicateKeyError as e:  # Except if it's already there
                print("Duplicate Key")
        count += len(new_tweets)
        print("Downloaded {0} tweets".format(count))
        max_id = new_tweets[-1].id

    except tweepy.TweepError as e:
        print("Rate Limit")

print("Downloaded {0} tweets. End of program".format(count))  # END OF FILE.
