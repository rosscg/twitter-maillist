from tweepy import OAuthHandler, Stream
from tweepy import API
from tweepy.streaming import StreamListener

from email_sender import send_email
from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKENS


class stream_listener(StreamListener):
    def on_status(self, status):
        try:
            text = status.extended_tweet.get('full_text')
        except:
            text = status.text
        print('Tweet detected: {}'.format(text))

        targets = [x[1] for x in ACCESS_TOKENS if x[2] == True]
        subject = 'Group message from: ' + status.user.screen_name
        message = 'From: ' + status.user.screen_name + '\n\n' + text

        send_email(targets, subject, message)
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

    # Get usernames in group
    followed = [x[0] for x in ACCESS_TOKENS]
    if len(followed) > 100:
        print("ERROR: Max list of users is 100")
        return
    # Get ids for screen names
    user_objects = api.lookup_users(screen_names=followed)
    user_ids = [user.id_str for user in user_objects]

    twitterStream = Stream(auth, stream_listener())
    twitterStream.filter(follow=user_ids, is_async=True)
    return


def post_tweet(token, message):
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(token[3], token[4])
    api = API(auth)
    api.update_status(status=message)
    return


def create_follow_network():
    print('Creating mutual follow-network for users')
    for user_data in ACCESS_TOKENS:
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(user_data[3], user_data[4])
        api = API(auth)
        for user_target in [x[0] for x in ACCESS_TOKENS if x != user_data]:
            print("Follower: {} Following: {}".format(user_data[0], user_target))
            try:
                api.create_friendship(user_target)
            except Exception as e:
                print(e)
                continue
    return


if __name__ == '__main__':
    create_follow_network()
