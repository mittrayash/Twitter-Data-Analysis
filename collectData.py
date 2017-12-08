import tweepy,pymongo

# Multiple auth keys for max query requests without exceeding rate limit.
authcount = 0
conskeys = ["A9TNLwxvBUF52slanuQMbbN4i","yKiP0AySVUpebAEqCTh8iYCjJ","QMqKeFUK3t86LdeWXkKEdHUT2","rHQ3rAswzTlerA4TCpFZDGota", "eet9COlNWAmhbQ93Qtw1N5qEo", "SBlZsM7ckoeECJtO6KSyfGscz", "tGLPkm7apTos0ObiYYX5Npvru", "w3oZSQnGxnpgZpME6VJyyFLBT", "GOVoDqdd4c9mC8Sr0l9nVAGuc", "dEj9PuikWT7amd5Ud5k79jurB"]
consecret = ["bahZEJNjhzEWRCVjW7xNMQRY9QCrKJBbKX97gleICO2KckqECm", "uIU1c1UntpU9SG3TSfKqkNhElWFHY7nw4WOjefaGNAOBaW5Baz", "G4ALtFOvrItBtXb3oW3runp5pUKtG7GNMebtowQH8twvXviXcI", "vR0usxrO4nDtyppdGbS48mlc4VenYqMBI235l8OKjXVytsbVYv", "WNrioh6Ufi7lsJJxiP8gYDg3uvaJvJPi2ZE4vG17PfxpjL9PFA", "rmkUPcEAWxi51ORC8O7NeujZIkZ0t3JSDyn8bkc7dtinDPDViS", "hbIUh2lqv4VibGqbQexN4CnuQmcKDTcedXJ1SDRWpPwQyyTo4H", "xFMNW2Xjz68maaFqpIGgSyPugtHzZan01mmZT4bWdPGypk2DU0", "YhJfSGIQVAialn57VaCEoJDt6Mm3QEyN57T6QkGt8488wveHVQ", "5nGkmWffNKIepE5bKjzj6RNLn0RTjjjLgxeVFp19ZLFwcOP40H"]
acctok = ["767202674-wic4r5VrnMwj6Wd82pfOmdwRUXndkh0eRizMt85H", "767202674-bUPVAz4mFB01jXeQrO9MWa2UqG4LLcrverRF6kTS", "767202674-5qIMo6VNUYwD2mvx938jmVgIBdnaNichLqlqGET5", "767202674-DXI7QMAnXDI9R5T7i5fqn4pfY2HWSeabxa8IZwlQ", "540132172-MvnOhI7dCQFYyLsuHrQ9qfBfU50v4vjnYqsrbJ9m", "540132172-G5uhArRvk7rZlRwkKDaiQVS69nITODidQrnSePmp", "540132172-nf0mglx8a5rTl8X71rJt0aYRFQO4KQBZyCXKlStj", "895015384507498496-Te9NDjdEGJCkBZRC0ctcX2dHEOw1fPL", "895015384507498496-06X4sOhT1L1F9wgrIDOop8NOQNwdgvl", "895015384507498496-drN0ZC4fAcKZWG0uk4g1ACQvILaUECZ"]
acctoksecret = ["VfnhH8XxCnQJ7VfKWZbBpaP39EnuSlwsMcmRMt9512yX7", "Le9Xi3c4VHDg20a30Axa7PBXqGvBUoBE6eEqhONGtHMla", "0HLmWpmx84LeHHTjboOq0IZ9KzmeaUxpTlU6wXWjnZwJz", "v2rLvodmf9LxyAQtn0vVn76XYymaEz9lU2oywKuffmCtg", "En2iXEzONr0E3yCejwkrqHTOnD2KDRJ2WvRb8QRzqrb4t", "F0XVqmvKYxReEnjzMcKOq5rX8EAMCUBTWKomODuEbZNKP", "nwffryYyMEMni3xOA6SSylmgKJj8TsBvkzT3M8PkP5F4n", "aowhQRJbu8zNU5VntMFoKIaCEp0A4iY96Tvbwd8s3MrRr", "Dq7jEKzUcLln92jFRkj8bOraIsRoc0JHBnCmP9Ivzz29E", "rcpKoy7OnipvbnblpPwVamPVvJKoQGt5Ux88sUz1tn0Oj"]

# Authenticating...
auth = tweepy.OAuthHandler(conskeys[authcount], consecret[authcount])
auth.set_access_token(acctok[authcount], acctoksecret[authcount])
api = tweepy.API(auth)

# Two queries - use one by one to curate 20,000 entries [10k each for Delhi Air Pollution and Mumbai Rain]
# query = "#Smog OR #MyRightToBreathe OR #CropBurning OR #AirPollution OR #LetMeBreathe OR #DelhiAirQuality OR #DelhiSmog OR #DelhiPollution OR #OddEven OR #OddEvenScheme OR #SaveDelhiAir OR #DelhiAir"
query = "#MumbaiRains OR #mumbaiRainedout OR #MumbaiDrowning OR #CycloneOckhi OR #saveFisherMen OR #mumbaiFloods OR #bombayRain OR #rainingMumbai OR #mumbaiPouring"
maxTweets = 10  # Work this program twice for the two queries - go one by one
tpq = 100  # Tweets per query1
max_id = -1  # Setting a max_id to remove redundancy in case any of the queries raise an exception
count = 0

client = pymongo.MongoClient()
db = client.abc
coll = db.all_tweets  # Setting collection to enter documents.

while count < maxTweets:  # To keep the extraction running even if exception is raised.
    try:
        if max_id < 0:
            new_tweets = api.search(q=query, count=tpq, tweet_mode="extended") # For the first time
        else:
            new_tweets = api.search(q=query, count=tpq, max_id=str(max_id-1), tweet_mode="extended") # After a max_id has been set.
        if not new_tweets:
            print("END OF TWEETS")  # If we exhaust all the tweets.
            break
        for tweet in new_tweets:
            # Collecting data from the tweet JSON we require to process later
            id = tweet.id_str
            user = tweet.user.name
            try:
                x = tweet.retweeted_status  # Can't be accessed if not retweet.
                RT = True
            except AttributeError:  # Hence this ^^
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
            try:
                md = tweet.entities["media"]
                media = []
                for i in md:
                    media.append(i["url"]) # And list of media (photos only)
            except KeyError: # If no media found
                media = []
            try:
                jsonx = {"_id": id, "user": user, "content": content, "timestamp": timestamp, "location": location,
                         "hashtags": hashtags, "media": media, "Retweet": RT, "Fav": fav} # Making a JSON to be sent to collection.
                coll.insert_one(jsonx)  # And insert
            except pymongo.errors.DuplicateKeyError as e:  # Except if it's already there
                print("Duplicate Key")
        count += len(new_tweets)
        print("Downloaded {0} tweets".format(count)) # Don't mind me, just keeping track.
        max_id = new_tweets[-1].id  # Max ID set as ID of last element in iterator.

    except tweepy.TweepError as e:  # In case 15k+ tweets done, rate limit. Switch user to carry on.
        print("Changing User")
        authcount = (authcount + 1) % 10
        auth = tweepy.OAuthHandler(conskeys[authcount], consecret[authcount])
        auth.set_access_token(acctok[authcount], acctoksecret[authcount])
        api = tweepy.API(auth)  # Re authentication
print("Downloaded {0} tweets. End of program".format(count))  # END OF FILE.
