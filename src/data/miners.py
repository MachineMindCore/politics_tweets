from time import strptime
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from logging import StreamHandler
from itertools import islice
import pandas as pd
import numpy as np
import json
import re
import inspect
import os
from datetime import datetime

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

  #Data loaders
  def to_content(self, tweets):
    collection = []
    for tweet in tweets:
      collection += [f"{tweet.created_at}: \n {tweet.full_text}"]
    return collection

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

  #Data handles
  def filter_by_date(self, tweetsRaw, interval: list):
    min_date = datetime.strptime(interval[0], "%Y-%m-%d")
    max_date = datetime.strptime(interval[1], "%Y-%m-%d")
    collection = {}
    for tweet in tweetsRaw:
      date = tweet.created_at
      if date > min_date and date < max_date:
        content = tweet.full_text
        if not (str(date) in collection.keys()):
          collection[str(date)] = []
        collection[str(date)] += [content]
    return collection

  def filter_by_match(self, tweetsRaw, matchObj: list):
    collection = {}
    for tweet in tweetsRaw:
      content = tweet.full_text
      date = tweet.created_at
      for word in matchObj:
        if word in content:
          if not (word in collection.keys()):
            collection[word] = []
          collection[word] += [f"{date}:\n {content}"]
    return collection

  def tweet_counter(self, target: str):
    semi_it = Cursor(
      self.api.user_timeline, 
      self.api.mentions_timeline, 
      screen_name=target, 
      tweet_mode="extended", 
      include_rts = False,
    )
    return len(list(semi_it.items()))
  
  def count(self, Obj, target):
    if target in Obj.keys():
      print(f"{target}: {len(Obj[target])}")
    else:
      print(f"{target}: {0}")
    return

  def retrieve_name(self):
    for name, value in globals().items():
      if value is self and not name.startswith('_'):
        return name

  def check_dir(self, dir):
    if not os.path.exists(dir):
      os.mkdir(dir)
    return

  def write_data(self, data, file):
    dir = "extract/"
    file = dir + file
    self.check_dir(dir)
    if type(data) == str:
      with open(file, "w") as f:
        f.write(data)
        f.close()
    elif type(data) == list:
      data = list(map(lambda d: d+"\n\n", data))
      with open(file, "w") as f:
        f.writelines(data)
        f.close()
    elif type(data) == dict:
      for key in data.keys():
        data[key] = list(map(lambda d: "    "+d+"\n\n", data[key]))
        with open(file, "a") as f:
          f.write("["+str(key)+"]"+"\n")
          f.writelines(data[key])
          f.close()
    else:
      print(f"Trying to write unsupported data type in {file}")
    return

  def save_tweets(self):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d_%H:%M:%S")
    name = self.retrieve_name()
    file_content = name + "_content" + f'-{current_time}.txt'
    file_match = name + "_match" + f'-{current_time}.txt'
    file_date = name + "_date" + f'-{current_time}.txt'
    self.write_data(self.tweets_content, file_content)
    self.write_data(self.tweets_date, file_date)
    self.write_data(self.tweets_match, file_match)
    return