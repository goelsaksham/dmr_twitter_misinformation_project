import tweepy
import sys
import time
import TwitterKeys as tk


def get_api_auth():
    """
    :return: The api type object after authorizing the api using the keys in the TwitterKeys file
    """
    auth = tweepy.OAuthHandler(tk.CONSUMER_KEY, tk.CONSUMER_SECRET)
    auth.set_access_token(tk.ACCESS_TOKEN, tk.ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,
                 retry_count=5, retry_delay=5, retry_errors= 54)
    return api


def generate_friends_list(user_id):
    """
    :param user_id: User ID of some twitter user (Numeric)
    :return: A list of user id's corresponding to the users which are being followed by the user corresponding to the
    user id passed as the parameter to the function.
    """
    api = get_api_auth()
    friend_user_ids = []
    for page_fr in tweepy.Cursor(api.friends_ids, user_id=user_id, count=5000).pages():
        friend_user_ids.extend(page_fr)
        time.sleep(5)
    return friend_user_ids


def main(user_id):
    try:
        return generate_friends_list(user_id)
    except:
        print("Error faced when finding data about:", user_id)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[-1])
    else:
        main(911271920842223617)