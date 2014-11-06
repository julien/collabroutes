import json, logging, utils, webapp2
from google.appengine.api import users
from utils import render_json

""" a request handler only used for testing """
class UserHandler(webapp2.RequestHandler):
  
  def get(self, *args, **kwargs):
    results = None
    user = users.get_current_user()
    if user:
      results = { 
        'user': {
          'nickname': user.nickname(), 
          'email': user.email()
        },
        'url': users.create_login_url(self.request.path)
      }
    else:
      results = { 
        'user': None, 
        'url': users.create_logout_url(self.request.path)
      }

    return utils.render_json(self, results)


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([(r'/user', UserHandler)], debug = True)
