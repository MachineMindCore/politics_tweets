from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from itertools import islice

class TweetParser:
  
  #Constructor
  def __init__(self, key, secret_key, token, secret_token):
    self.API_KEY = key
    self.ACCESS_TOKEN = token
    self.API_SECRET_KEY = secret_key
    self.ACCESS_TOKEN_SECRET = secret_token
    self.auth = OAuthHandler(self.API_KEY, self.API_SECRET_KEY)
    self.auth.set_access_token(token, secret_token)
    self.api = API(self.auth, wait_on_rate_limit=True)
    #self.data = self.__load__()
    return

  def __load__(self):
    self.data = self.api.me()
    return

  def get_full(self, target: str): 
    tweet_it = Cursor(
      self.api.user_timeline, 
      screen_name=target,
      tweet_mode="extended", 
      include_rts = False,
    ).items()

    collection = []
    for tweet in tweet_it:
      try:
        collection += [tweet]
      except:
        print("time out")
        break
    return collection

  def get_by_number(self, target: str, start=0, stop=None): 
    limit=1000
    stop = start+limit-1 if stop==None else stop
    tweet_it = Cursor(
      self.api.user_timeline, 
      screen_name=target,
      tweet_mode="extended", 
      include_rts = False,
    ).items()

    collection = []
    for tweet in islice(tweet_it, start, stop):
      try:
        collection += [tweet]
      except:
        print("overindexed iterator")
        break
    return collection
