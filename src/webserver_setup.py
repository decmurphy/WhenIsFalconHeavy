# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import praw

r = praw.Reddit('OAuth testing example by u/_Daimon_ ver 0.1 see '
                'https://praw.readthedocs.org/en/latest/'
                'pages/oauth.html for source')
                
r.set_oauth_app_info(client_id='xXqevuNhLwdGEg',
                client_secret='50GEgWLy7tMyE1N9wbV70TfBGHw',
                redirect_uri='http://127.0.0.1:65010/'
                'authorize_callback')

url = r.get_authorize_url('uniqueKey', 'identity', True)
                
import webbrowser
webbrowser.open(url)
# click allow on the displayed web page