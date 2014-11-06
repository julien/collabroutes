import webapp2

class MainHandler(webapp2.RequestHandler):

  def get(self):
    if self.request.url.endswith('/'):
      path = '%sindex.html' % self.request.url
      self.redirect(path)

  def post(self):
      self.get()
 
app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)

