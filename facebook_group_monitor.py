# I beleive this won't return posts which have a user tagged in them, but yet to test.
# Not possible to get author of message due to API privacy limitations.
# Access token must be from a member of the group.
# Comments on posts are not returned when using a user access token, need app
# token for this, which requires app review from Facebook.

from datetime import datetime
import facebook
import requests
from time import sleep

from email_sender import send_email
from credentials import FACEBOOK_ACCESS_TOKEN

group_page_id = "FACEBOOK_PAGE_ID"
email_list = ["EMAIL_ADDRESS", "EMAIL_ADDRESS_2_etc"]
        # TODO: Store email_list list as a file, and update file by checking
        # email for subscribe/unsubscribe emails in smtp mailbox.
        # https://stackoverflow.com/questions/18156485/receive-replies-from-gmail-with-smtplib-python
email_subject = "EMAIL SUBJECT LINE"

def get_page_posts(page_id):
    access_token = FACEBOOK_ACCESS_TOKEN
    graph = facebook.GraphAPI(access_token)
    posts_gen = graph.get_all_connections(page_id, "feed")

    # Get the previously stored latest_post_time, if exists.
    try:
        file = open('last_fb_post_time.txt','r')
        saved_post_time = file.readline()
        saved_post_time = datetime.strptime(saved_post_time, "%Y-%m-%d %H:%M:%S%z")
        ###### TESTING:
        #saved_post_time = datetime.strptime("2014-01-03 01:12:20+00:00", "%Y-%m-%d %H:%M:%S%z")
        file.close()
    except Exception as e:
        print(e)
        # Use timezone.now for all posts after init:
        #saved_post_time = datetime.now().replace(tzinfo=timezone.utc)
        # Use for all historical posts:
        saved_post_time = datetime.strptime("1900-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")

    # Store most recent post from returned data, to store for next check.
    latest_post_time = None

    for post in posts_gen:
        post_date = datetime.strptime(post.get("updated_time"), "%Y-%m-%dT%H:%M:%S%z")
        if post_date > saved_post_time:
            # Handle data here.
            message = post.get("message") # a None value is likely a 'story' rather than a post - eg. update to group name.
            if message is not None:
                post_link = 'https://www.facebook.com/' + post.get("id") # URL to post
                #send_email(email_list, email_subject, (message + '\n\nSource: ' + post_link))
            if latest_post_time is None or post_date > latest_post_time:
                    latest_post_time = post_date

    # Write latest_post_time to file
    if latest_post_time is not None and latest_post_time > saved_post_time:
        file = open('last_fb_post_time.txt','w+')
        file.write(str(latest_post_time))
        file.close()


if __name__ == '__main__':

    #while True:
    #    print('Checking group for new posts...')
    get_page_posts(group_page_id)
        #sleep(60)
