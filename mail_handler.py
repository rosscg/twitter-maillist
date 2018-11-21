
from email_sender import send_email
from credentials import ACCESS_TOKENS, ADMIN_EMAIL
from twitter_functions import post_tweet

def tweet_message(sender, text):
    print("Received message from:\n{}".format(sender))
    # Check length of message
    if len(text) > 280:
        print("Message is too long.")
        message = 'Message rejected: Over 280 characters ({}):\n\n{}'.format(len(text), text)
        send_email(sender, 'Message Rejected', message)
        return False
    try:
        token = [x for x in ACCESS_TOKENS if x[1] == sender][0]
    except Exception as e:
        print("Email received from unauthorised address: {}".format(sender))
        message = 'No Twitter account attached to email: {}\nContact the administrator of this bot: {}'.format(sender, ADMIN_EMAIL)
        print(message)
        send_email(sender, 'Message Rejected', message)
    # Post to Twitter.
    post_tweet(token, text)
    return True
