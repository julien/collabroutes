"""
A very basic test example.
Can be used as a "boilerplate"
"""
import unittest

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed


class TestModel(db.Model):
  """ model used for testing """
  number = db.IntegerProperty(default=42)
  text = db.StringProperty()

 
class TestEntityGroupRoot(db.Model):
  """ entity group root """
  pass

def GetEntityViaMemcache(entity_key):
  entity = memcache.get(entity_key)

  if entity is not None:
    return entity

  entity = TestModel.get(entity_key)

  if entity is not None:
    memcache.set(entity_key, entity)
  
  return entity

class DemoTestCase(unittest.TestCase):

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def testInsertEntity(self):
    TestModel().put()
    self.assertEqual(1, len(TestModel.all().fetch(2)))


if __name__ == '__main__':
  unittest.main()


