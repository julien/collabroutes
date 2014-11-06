import json, logging, utils, webapp2
from models.trip import TripSearch

class SearchHandler(webapp2.RequestHandler):
  # read
  def get(self, *args, **kwargs):
    results = []
    if args and len(args) == 2:
      try:
        searchId = int(args[1])
      except ValueError:
        utils.render_json(self, {'error': 'invalid search'})
        return
        
      search = TripSearch.get_by_id(searchId)
      if search:
        results = search.to_dict()
      else:
        utils.render_json(self, {'error': 'search not found'})
        return

    else:
      searchs = TripSearch.query()
      results = []
      for search in searchs:
        results.append(search.to_dict())
    
    utils.render_json(self, results)

  # create
  def post(self):
    results = {}
    try:
      body = json.loads(self.request.body)
      search = TripSearch()
      utils.setattrs(search, body)
      search.put()
      results = search.to_dict()
    except ValueError:
      results = {'message': 'an error occured'}

    utils.render_json(self, results)
 

  # update
  def put(self):
    results = {}
    try:
      body = json.loads(self.request.body)
      if body.has_key('id'):
        search = TripSearch.get_by_id(body['id'])
        if search:
          utils.setattrs(search, body)
          search.put()
          results = search.to_dict()
        else:
          results = {'message': 'search not found'}
      else:
        results = {'message': 'id not received'}
    except ValueError:
      results = {'message': 'an error occured'}

    utils.render_json(self, results)

  # delete
  def delete(self):
    results = {}
    try:
      body = json.loads(self.request.body)
      if body.has_key('id'):
        search = TripSearch.get_by_id(body['id'])
        if search:
          search.key.delete()
          results = {'message': 'deleted'}
        else:
          results = {'message': 'search not found'}
      else:
        results = {'message': 'id not received'}
    except ValueError:
      results = {'message': 'an error occured'}
      
    utils.render_json(self, results)


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([
  (r'/search', SearchHandler),
  (r'/search(\/)(.*?)', SearchHandler)  
  ], debug=True)


