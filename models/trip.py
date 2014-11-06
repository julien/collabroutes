import datetime
from google.appengine.ext import ndb

class TripReview(ndb.Model):
  date = ndb.DateProperty(auto_now_add = True)
  content = ndb.TextProperty(required = True)

class TripSearch(ndb.Model):
  date = ndb.DateProperty(auto_now_add = True)
  destination = ndb.StringProperty(required = True)
  origin = ndb.StringProperty(required = True)
  places = ndb.IntegerProperty(default = 1)
  user = ndb.UserProperty(auto_current_user_add = True)

  def to_dict(self):
    d = {
      'date': str(self.date),
      'destination': self.destination,
      'origin': self.origin,
      'places': self.places,
      'user': str(self.user),
      'id': self.key.id() if self.key else None
    }
    return d

  @staticmethod
  def find_offers(search, limit = 30):
    if type(search) is TripSearch:
      origin = search.origin
      destination = search.destination
      places = search.places
      date = search.date
    elif type(search) is dict:
      origin = search['origin']
      destination = search['destination']
      places = search['places']
      split = search['date'].split('-')
      date = datetime.date(int(split[0]), int(split[1]), int(split[2]))
    else:
      pass
   
    results = TripOffer.query(ndb.OR(
      TripOffer.origin == origin, 
      TripOffer.destination == destination),
      TripOffer.availability >= places,
      TripOffer.date == date)

    return results.fetch(limit)

class TripOffer(ndb.Model):
  availability = ndb.IntegerProperty(default = 1)
  date = ndb.DateProperty(auto_now_add = True)
  description = ndb.TextProperty()
  destination = ndb.StringProperty(required = True)
  fees = ndb.FloatProperty(default = 0)
  origin = ndb.StringProperty(required = True)
  reviews = ndb.StructuredProperty(TripReview, repeated = True)
  pending_orders = ndb.StructuredProperty(TripSearch, repeated = True)
  confirmed_orders = ndb.StructuredProperty(TripSearch, repeated = True)
  user = ndb.UserProperty(auto_current_user_add = True)

  def to_dict(self):
    d = { 
      'availability': self.availability,
      'date': str(self.date),
      'description': self.description,
      'destination': self.destination,
      'fees': self.fees,
      'origin': self.origin,
      'user': str(self.user),
      'id': self.key.id() if self.key else None
    }
    return d
  
  @staticmethod
  def add_offer(offer, search):
    index = None
    try:
      index = offer.pending_offers.index(search)
      pass
    except ValueError:
      pass

    if index is None:
      offer.pending_offers.append(search)
      return offer.pending_offer

  @staticmethod
  def find_searches(offer, limit = 30):
    if type(offer) is TripOffer:
      origin = offer.origin
      destination = offer.destination
      date = offer.date
      availability = offer.availability
    elif type(offer) is dict:
      origin = offer['origin']
      destination = offer['destination']
      split = offer['date'].split('-')
      date = datetime.date(int(split[0]), int(split[1]), int(split[2]))
      availability = offer['availability']
    else:
      pass

    results = TripOffer.query(ndb.OR(        
      TripSearch.origin == origin,  
      TripSearch.destination == destination),
      TripSearch.date == date,
      TripSearch.places <= availability)

    return results.fetch(limit)

