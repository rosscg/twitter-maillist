# This server allows users to authorise the app to use their Twitter
# credentials. Their token is written to the credentials.py file.
#
# To run:
# $ export FLASK_APP=flask_twitter_auth.py
# $ flask run

from flask import Flask, session, redirect, request
import tweepy

from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKENS

app = Flask(__name__)
app.secret_key = 'akjdsks112kjakjdsks112kj'
callback = 'http://127.0.0.1:5000/callback'
form_template='<form method=\"POST\"><b>Email Address:<input name=\"text\">Recieve emails:<input type="checkbox" name="subscribe" checked><input type=\"submit\"></b></form>'


@app.route('/')
def my_form():
    try:
        t = session['token'] # Authenticated, ask for email.
    except KeyError as e: # Not authenticated
        return redirect('/auth')
    return form_template


@app.route('/', methods=['POST'])
def my_form_post():
    subscribe =  "subscribe" in request.form
    # Get info from existing credentials file:
    try:
        cred_file = open('credentials.py','r+')
    except:
        return 'Error with credentials file'
    if session['screen_name'].lower() in [x[0].lower() for x in ACCESS_TOKENS]:
        return "Username credentials already exist"
    cred_lines = cred_file.readlines()
    cred_file.close()
    try:
        x = session['token']
    except:    # KeyError if user refreshes form.
        return redirect('/')
    # Overwrite credentials file with addition of new token.
    new_cred_file = open('credentials.py','w+')
    for line in cred_lines[:len(cred_lines)-1]:
        new_cred_file.write(line)
    new_cred_file.write("    ('{}', '{}', '{}', '{}', '{}'),\n".format(session['screen_name'], request.form['text'].lower(), subscribe, session['token'][0], session['token'][1]))
    new_cred_file.write('    )\n')
    new_cred_file.close()
    del session['token']
    return "<b>Added:\n{}\n{}</b>".format(session['screen_name'], request.form['text'].lower())


@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)


@app.route('/callback')
def twitter_callback():
    request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)
    session['screen_name'] = auth.get_username()
    return redirect('/')
