import praw
import time
import datetime
import MySQLdb
import dbprops
import ConfigParser

from dateutil.relativedelta import relativedelta

from flask import Flask
from flask import request
app = Flask(__name__)

Config = ConfigParser.ConfigParser()
Config.read('praw.ini')
CLIENT_ID = Config.get('prod','client_id')
CLIENT_SECRET = Config.get('prod','client_secret')
REDIRECT_URI = Config.get('prod','redirect_uri')

access_information = ''

db = MySQLdb.connect(host=dbprops.host, # your host, usually localhost
                      port=dbprops.port,
                      user=dbprops.user, # your username
                      passwd=dbprops.password, # your password
                      db=dbprops.database) # name of the data base
                      
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
    already_done = []

    cur = db.cursor()
    cur.execute("""SELECT month, year FROM Date;""")

    row = cur.fetchone()
    month = row[0]
    year = row[1]
    
    orig_date = datetime.date(year, month, 1)
    date = orig_date
    one_month = relativedelta(months=1)

    while True:
      try:
        time.sleep(120)
        comments_by_sub = r.get_comments('spacex',limit=20)
        for comment in comments_by_sub:
            if comment.author is not None:
                if 'falcon heavy' in comment.body.lower() and comment.id not in replied:
                    date = date + one_month
                    executeQuery = "UPDATE Date SET year=%d, month=%d;" % (date.year, date.month)
                    cur.execute(executeQuery)
                    db.commit()
                    new_comment = comment.reply('You mentioned Falcon Heavy. By doing so you have '
                        'pushed the NET date one month into the future. The new '
                        'NET is {month} {year}.\n\n---\n\n^(I am a bot. If you have feedback, please message /u/TheVehicleDestroyer)'
                        .format(month=date.strftime("%B"), year=date.year))
                    replied.append(comment.id)
                    replied.append(new_comment.id)
        
      except praw.errors.OAuthInvalidToken:
        
        access_information = r.refresh_access_information(access_information['refresh_token'])

      except praw.errors.RateLimitExceeded:

        print 'caught RateLimitExceeded error'

    return "Activation finished"


if __name__ == '__main__':
    
    r = praw.Reddit('Date counter app by /u/WhenIsFalconHeavy v1.0')
    r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    app.run(debug=True,host='0.0.0.0')
