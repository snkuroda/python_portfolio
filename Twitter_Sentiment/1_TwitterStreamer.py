import tweepy, json, sqlite3, dataset, time
from tweepy.streaming import StreamListener
import pandas
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia

# Set Twitter credentials

auth = tweepy.OAuthHandler('v2yq8Vzz2gZNAMCMUCuuOsS48', 'ZpZalEZAS5SGlT9BRqvnrAv0WLwREL6P7j6xs03lyOxs6wwnvP')
auth.set_access_token('2210303246-tNlKafJ5snj5XqYRrLRF3TxdJJWzvo6ZMiDYJXc', 'xa0yixDQCUzHaE8PBP8SD1ah8O116azikY6Tmr6AaGTAJ')

# Workspace for tweets - SQLite database (use dataset lib to imprt schema)
db = dataset.connect("sqlite:///tweets.db") # Create a data database, create one if none exists


### Query Twitter
class Streamer(StreamListener):

    def on_status(self, status):

        try:
            if status.coordinates != None and status.place.country_code == 'US' and status.retweeted == False:
                id_str = status.id_str # ID given to specific tweet
                name = status.user.screen_name # Name of Tweeter
                created = status.created_at # When the tweet was sent
                text = status.text # The tweet
                
                coords = status.coordinates # Coordinates from where the tweet was sent
                coords = json.dumps(coords) # drops the coords from json to string, so it can be stored in sql
                # Add sentiment analysis
                sid = sia()
                polarity = sid.polarity_scores(text)["compound"] # Set sentiment score to "polarity" object
                if polarity != 0.0:    

                    #Store Tweets into SQLite db
                    table = db["tweets"]
                    table.insert(dict(
                        tweet_id=id_str,
                        user=name,
                        tweet_datetime=created,
                        text=text,
                        sentement_score=polarity,
                        coords = coords,
                        ))
                    print("Tweet Added", text)
        except TypeError:
            print('e')
            pass

                
    def on_error(self, status):
        print(status)
    


# Set Bounding box to isolate geotagged tweets. Set to Lower 48 of the US.
US_bounds = [-133.0,25.3,-59.7,50.8]

# Call the Streaming service, pass the authorizing credentials
# Call the query using the filter 
def start_stream():
    while True:
        try:
            twitter_stream = tweepy.Stream(auth, Streamer())
            twitter_stream.filter(locations=US_bounds, stall_warnings=True)
        
        except:           
            continue
        

start_stream()

