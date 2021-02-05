
# # # # IMPORT MODULES # # # #
import tweepy
import dataset
from tweepy import OAuthHandler
from textblob import TextBlob
import json
from datetime import datetime



# CREATE CLASS twitterAuthenticator():
#     """
#     Authenticating Dev Tweet Account credentials...


def authenticate_twitter():
    auth = OAuthHandler('cZ7Qy0lZvAA2VkdejjHeZ2tg7', '4empMR98EwcdlSk26nzNM4h3g1H9l1oOkc8QAelryDASLBJQE7')
    auth.set_access_token('1340376549099331584-5ix6mutS3Qh1rhdne06sZvsrAuv5TN', 'JxzukBLAkg0ZFnnNyXfX9xNTuEpYBNdwanLk7UjpFqsuY')
    api = tweepy.API(auth)
    return api

#### GET TWEETS...####
# CREATE CLASS GetFromTwitter():
    # """
    # Class for retrieving tweets using keywords
    # """

def get_tweets(query, num_tweets):
    api = authenticate_twitter()
    json_tweet_list = [status._json for status in tweepy.Cursor(api.search, q=query, chose_lang='english').items(num_tweets)]

    return json_tweet_list






# # # # CLEAN THE TWEETS # # # #
# DEFINE FUNCTION clean_tweets(created_list_for_tweets):
#     created_list_for_clean_tweets = []
#     iterate over created_list_for_tweets:
#         append clean tweets using(clean(tweet))
def store_tweets(json_tweet_list, db):
    for tweet_json in json_tweet_list:
        try:
            table = db["tweets"]
            tweet = tweet_json['text'],

            print(tweet_json['created_at'])
            table.insert(dict(
                tweet_id = tweet_json['id_str'],
                user_id = tweet_json['user']['id_str'],
                user_nm = tweet_json['user']['name'],
                tweet_dt = datetime.strptime(tweet_json['created_at'], ),
                tweet_txt = tweet,
                sentiment_score = None)
            )

            print("Tweet Added", tweet_txt)

        except Exception as err:
            print(err)
            pass

#
# # # # # GET  SENTIMENTS... # # # #
# DEFINE FUNCTION get_sentiments(created_list_for_clean_tweets):
#     create_list_for_sentiment_score = []
#     iterate over created_list_for_clean_tweets:
#         create variable - score that = use 'TextBlob' to convert tweet to do "NLP", using TextBlob(tweet)
#         # sentiment.polarity check if positive or negative
#         append variable - score to the create_list_for_sentiment_score using variable - score.sentiment.polarity
#
#     return variable - score
#
#
# ...TO CONTINUE

def create_db(db_name):
    database = dataset.connect(f"sqlite:///{db_name}.db")  # Create a data database, create one if none exists

    return database


def main():
    q = "#pdx911"

    authenticate_twitter()
    tweets = get_tweets(q, 10)
    db = create_db("pdx_tweets")
    store_tweets(tweets, db)
    # get_sentiments()
    # Store tweets



if __name__ == "__main__":
    main()