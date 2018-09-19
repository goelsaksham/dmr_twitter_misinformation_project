import tweepy
import os
import sys
import json
import datetime
import TwitterKeys as tk
import FileAndDirectoryNames as info
import QueryGenerator as qg


def get_api_auth():
    """
    :return: The api type object after authorizing the api using the keys in the TwitterKeys file
    """
    auth = tweepy.OAuthHandler(tk.CONSUMER_KEY, tk.CONSUMER_SECRET)
    auth.set_access_token(tk.ACCESS_TOKEN, tk.ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,
                 retry_count=5, retry_delay=5, retry_errors= 54)
    return api


def get_now():
    """
    :return: The now type object which defines the upper range of the date till which the tweets should be collected
    """
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d")
    return now


def collect_tweets_for_query(dir_path, query_for_tweets, file_format='.json'):
    """
    :param dir_path: The directory in which the file will be stored
    :param query_for_tweets: The query which will be used to collect the tweets
    :param file_format: The file format in which the tweet data will be saved
    :return: N/A
    Creates a file of the specified file format in the specified directory.
    This file will contain the tweets that are collected using the Twitter API
    which correspond to the query posed.
    """
    if os.path.exists(dir_path):
        with open(dir_path + query_for_tweets + file_format, 'w') as file_writer:
            api = get_api_auth()
            now = get_now()
            number_of_tweets = 0
            for tweet in tweepy.Cursor(api.search, q=query_for_tweets,
                                       count=100, lang="en", until=now).items():
                tweet = tweet._json
                tweet = json.dumps(tweet)
                file_writer.write(tweet+'\n')
                number_of_tweets += 1
        print("File Generated:", dir_path + query_for_tweets + file_format,
              ", Total Number of Collected Tweets:", number_of_tweets)
    else:
        print("Invalid directory path:", dir_path)


def main(dir_path, query_for_tweets, file_format):
    collect_tweets_for_query(dir_path, query_for_tweets, file_format)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[-3], sys.argv[-2], sys.argv[-1])
    else:
        main(info.Search_Tweet_Output_Directory,
             qg.query_generator(info.Query_For_Tweet),
             info.Tweet_Output_File_Format)