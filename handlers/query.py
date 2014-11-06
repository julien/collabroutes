import datetime, json, logging, utils, webapp2
from models.trip import TripOffer, TripSearch

class QueryHandler(webapp2.RequestHandler):
  def get(self):
    pass
 
  def post(self):
    results = []
    if self.request.body:
      body = json.loads(self.request.body)
      search = {}
      if body.has_key('origin') and body.has_key('destination'):
        search['origin'] = body['origin']
        search['destination'] = body['destination']
        search['date'] = body['date'] if body.has_key('date') else str(datetime.date.today())
        search['places'] = body['places'] if body.has_key('places') else 1

        search_results = TripSearch.find_offers(search)
        for result in search_results:
          results.append(result.to_dict())

    utils.render_json(self, results)


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([(r'/query', QueryHandler)], debug=True)

