import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User

TWITTER_USERS = ['elonmusk', 'nasa', 'sadserver', 'austen', 'lockeedmartin']

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_API_KEY'),
                                   config('TWITTER_CONSUMER_API_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(config('BASILICA_KEY'))


def add_user(name):
    """Adds a user along with their tweet to our database."""
    try:
        # Using tweepy API to get user info
        twitter_user = TWITTER.get_user(name)

        # Add user info to user table in database
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                   name=name,
                   followers=twitter_user.followers_count))
        DB.session.add(db_user)

        # Adding recent non-retwee/reply tweets
        # the limmit on Twitter API is 200 for single request
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
         
            emb = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=emb)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f'Encountered error while processing {name}: {e}')
        raise e
    else:
        DB.session.commit()


def add_default_users(users=TWITTER_USERS):
    for user in users:
        add_user(user)


def update_all_users():

    for user in User.query.all():
        add_user(user.name)
