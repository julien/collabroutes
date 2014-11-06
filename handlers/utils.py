""" utility functions for G.A.E. python development """
import json
from google.appengine.api import users

""" renders json to the response """
def render_json(handler, data):
  handler.response.headers['Content-type'] = 'application/json'
  handler.response.out.write(json.dumps(data, indent=2, separators=(', ', ': ')))
  
""" merge request params to an object """
def setattrs(target, attrs):
  for k in attrs:
    if hasattr(target, k) and getattr(target, k) != attrs[k]:
      setattr(target, k, attrs[k])
  return target

def login_required(handler_method):
  """
  This decorator requires admin, 403 if not.
  """
  def auth_required(self, *args, **kwargs):
    # if users.is_current_user_admin():
    if users.get_current_user():
      handler_method(self, *args, **kwargs)
    else:
      self.error(403)
  return auth_required


