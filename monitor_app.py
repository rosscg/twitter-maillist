# Adapted from: https://gist.github.com/nickoala/569a9d191d088d82a5ef5c03c0690a02
# May have to allow 'less secure apps' in Gmail
import re
import time
import imaplib
import email
from itertools import chain

from mail_handler import tweet_message
from twitter_functions import monitor_stream
from credentials import USERNAME, PASSWORD, ACCOUNT_NAME

imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
imap_ssl_port = 993

mail_refresh_rate = 5

# Filtering criteria (unneeded for this use)
criteria = {
    #'FROM':    'EMAIL ADDRESSES',
    #'SUBJECT': 'SPECIAL SUBJECT LINE',
    #'BODY':    'SECRET SIGNATURE',
}


def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))


def get_first_text_block(msg):
    type = msg.get_content_maintype()
    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload().strip()
    elif type == 'text':
        return msg.get_payload().strip()

try:
    # Get last uid returned from file.
    file = open('max_uid.txt','r')
    uid_max = int(file.readline())
    file.close()
except:
    uid_max = 0


# Start Twitter stream monitoring
monitor_stream()
print("Twitter stream started...")

# Start Mail monitoring
while True:
    print("Checking inbox...")

    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(USERNAME, PASSWORD)
    server.select('INBOX')

    typ, data = server.uid('search', None, search_string(uid_max, criteria))

    uids = [int(s) for s in data[0].split()]

    for uid in uids:
        # Have to check again because Gmail sometimes does not obey UID criterion.
        if uid > uid_max:
            result, data = server.uid('fetch', str(uid), '(RFC822)')  # fetch entire message
            msg = email.message_from_string(data[0][1].decode("utf-8"))
            uid_max = uid

            # Write last uid returned to file.
            file = open('max_uid.txt','w+')
            file.write(str(uid_max))
            file.close()

            text = get_first_text_block(msg)
            # Extracting email from string
            sender = re.search(r'\<(.*(?!>).)', msg['From']).group(1)

            try:
                tweet_message(sender, text)
            except Exception as e:
                print(e)


    server.close()
    server.logout()
    time.sleep(mail_refresh_rate)
