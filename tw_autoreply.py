# Follows a list of users and replies to all of their original Tweets with a
# randomly selected string. Ignores replies and retweets.
# Will probably be flagged and banned by Twitter as auto-responses violate
# Twitter's developer terms: https://developer.twitter.com/en/developer-terms/more-on-restricted-use-cases.html

import random

from tweepy import OAuthHandler, Stream
from tweepy import API
from tweepy.streaming import StreamListener

from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKENS


messages = ["Example reply message", "Example reply message 2"]
followed = ["example_screen_name"]


class stream_listener(StreamListener):
    def on_status(self, status):
        print('Tweet detected from user: {}'.format(status.user.screen_name))
        # Consider adding random delay.
        if status.in_reply_to_status_id or status.is_quote_status or status.retweeted_status:
            print('Tweet is a reply or retweet, ignoring.')
            return
        print('Replying to Tweet..')
        reply_to_tweet(random.choice(ACCESS_TOKENS), random.choice(messages), status)
        return

    def on_error(self, status_code):
        print("<<<<<<<< Error: {} >>>>>>>>>".format(status_code))
        if status_code == 420:
            return False
        return


def monitor_stream():
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKENS[0][3], ACCESS_TOKENS[0][4])
    api = API(auth)

    if len(followed) > 100: # Twitter limitation
        print("ERROR: Max list of users is 100")
        return

    print('Autoreplying to users: ', followed)
    user_objects = api.lookup_users(screen_names=followed)
    user_ids = [user.id_str for user in user_objects]

    twitterStream = Stream(auth, stream_listener())
    twitterStream.filter(follow=user_ids, async=True)
    return


def reply_to_tweet(token, message, original_status):
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(token[3], token[4])
    api = API(auth)

    message = message + ' ' + '@' + original_status.user.screen_name
    api.update_status(status=message, in_reply_to_status_id=original_status.id)
    return



if __name__ == '__main__':
    monitor_stream()
