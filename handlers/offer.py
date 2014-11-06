import json, logging, utils, webapp2
from models.trip import TripOffer
from utils import login_required

class OfferHandler(webapp2.RequestHandler):
  # read
  def get(self, *args, **kwargs):
    results = []
    if args and len(args) == 2:
      try:
        offerId = int(args[1])
      except ValueError:
        utils.render_json(self, {'error': 'invalid search'})
        return
        
      offer = TripOffer.get_by_id(offerId)
      if offer:
        results = offer.to_dict()
      else:
        utils.render_json(self, {'error': 'offer not found'})
        return

    else:
      offers = TripOffer.query(TripOffer.availability > 0)
      results = []
      for offer in offers:
        results.append(offer.to_dict())
    
    utils.render_json(self, results)

  # create
  @login_required
  def post(self):
    results = {}
    try:
      body = json.loads(self.request.body)
      offer = TripOffer()
      utils.setattrs(offer, body)
      offer.put()
      results = offer.to_dict()
    except ValueError:
      results = {'message': 'an error occured'}

    utils.render_json(self, results)
 

  # update
  @login_required
  def put(self):
    results = {}
    try:
      body = json.loads(self.request.body)
      if body.has_key('id'):
        offer = TripOffer.get_by_id(body['id'])
        if offer:
          utils.setattrs(offer, body)
          offer.put()
          results = offer.to_dict()
        else:
          results = {'message': 'offer not found'}
      else:
        results = {'message': 'id not received'}
    except ValueError:
      results = {'message': 'an error occured'}

    utils.render_json(self, results)

  # delete
  @login_required
  def delete(self):
    results = {}
    try:
      body = json.loads(self.request.body)
      if body.has_key('id'):
        offer = TripOffer.get_by_id(body['id'])
        if offer:
          offer.key.delete()
          results = {'message': 'deleted'}
        else:
          results = {'message': 'offer not found'}
      else:
        results = {'message': 'id not received'}
    except ValueError:
      results = {'message': 'an error occured'}
      
    utils.render_json(self, results)


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([
  (r'/offer', OfferHandler),
  (r'/offer(\/)(.*?)', OfferHandler)  
  ], debug=True)


