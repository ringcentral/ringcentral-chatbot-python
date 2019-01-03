import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from ringcentral_bot_framework.core.db import dbAction as action, DBNAME
import pydash as _

class TestFiledbMethods(unittest.TestCase):

  def test_basic_filedb(self):
    print('running filedb test')
    self.assertEqual(DBNAME, 'filedb')
    x = action('bot', 'add', {'s': 's', 'id': 'axx', 'dgfdf': [
      'sdfs', 'sdfsd'
    ]})
    self.assertEqual(x, 'add')
    x1 = action('bot', 'add', {'s': 's', 'id': 'bxx1', 'dgfdf': [
      'sdfs', 'sdfsd'
    ]})
    self.assertEqual(x1, 'add')
    x2 = action('bot', 'get', { 'id': 'bxx1'})
    self.assertEqual(x2['id'], 'bxx1')
    x2 = action('bot', 'update', { 'id': 'bxx1', 'update': {
      's': 45,
      'fg': 'sdf'
    }})
    x2 = action('bot', 'get', { 'id': 'bxx1'})
    self.assertEqual(x2['id'], 'bxx1')
    self.assertEqual(x2['s'], 45)
    self.assertEqual(x2['fg'], 'sdf')
    x2 = action('bot', 'get')
    xx2 = _.collections.find(
      x2,
      lambda x: x['id'] == 'bxx1'
    )
    self.assertEqual(xx2['fg'], 'sdf')

if __name__ == '__main__':
    unittest.main()