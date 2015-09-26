import praw
import time
import datetime

from dateutil.relativedelta import relativedelta

from flask import Flask
from flask import request
app = Flask(__name__)

CLIENT_ID = 'My4z-cA89mwPAA'
CLIENT_SECRET = 'S75z9JF0CKdLQUhyZvHBKUpfDto'
REDIRECT_URI = 'http://flask.decmurphy.com/authorize_callback'

access_information = ''

@app.route('/')
def homepage():
    link_refresh = r.get_authorize_url('DifferentUniqueKey','identity read submit', refreshable=True)
    link_refresh = "<a href=%s>link</a>" % link_refresh
    text = "Refreshable %s</br></br>" % link_refresh
    return text

@app.route('/authorize_callback', methods=['GET'])
def authorized():

    #pp = pprint.PrettyPrinter(indent=4)
    code = request.args.get('code', '')
    access_information = r.get_access_information(code)  
    activate()
    return "Success"

@app.route('/activate')
def activate():

    replied = []

    orig_date = datetime.date(2017, 1, 1)
    date = orig_date
    one_month = relativedelta(months=1)
    
    clock = 0
    
    while True:
        comments_by_sub = r.get_comments('test',limit=10)
        for comment in comments_by_sub:
            if comment.author is not None:
                if 'newtrigger' in comment.body.lower() and comment.id not in replied:
                    date = date + one_month
                    new_comment = comment.reply('You mentioned Trigger. By doing so you have '
                        'pushed the NET date one month into the future.\n\nThe new '
                        'NET is {month} {year}.\n\nThanks a lot.'
                        .format(month=date.strftime("%B"), year=date.year))
                    replied.append(comment.id)
                    replied.append(new_comment.id)
        
        time.sleep(5)
        
        clock = clock + 5
        if clock > 3000:
            r.refresh_access_information(access_information['refresh_token'])
            clock = clock - 3000

    return "Activation finished"


if __name__ == '__main__':
    
    r = praw.Reddit('Date counter app by /u/WhenIsFalconHeavy v1.0')
    r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    app.run(debug=True, host='0.0.0.0')
