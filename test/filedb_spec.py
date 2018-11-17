import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from core.filedb import action

class TestStringMethods(unittest.TestCase):

    def test_basic(self):
      x = action('bot', 'add', {'s': 's', 'id': 'xss', 'dgfdf': [
        'sdfs', 'sdfsd'
      ]})
      self.assertEqual(x, 'add')
      x1 = action('bot', 'add', {'s': 's', 'id': 'xss1', 'dgfdf': [
        'sdfs', 'sdfsd'
      ]})
      self.assertEqual(x1, 'add')
      x2 = action('bot', 'get', { 'id': 'xss1'})
      self.assertEqual(x2['id'], 'xss1')
      x2 = action('bot', 'update', { 'id': 'xss1', 'update': {
        's': 45,
        'fg': 'sdf'
      }})
      x2 = action('bot', 'get', { 'id': 'xss1'})
      self.assertEqual(x2['id'], 'xss1')
      self.assertEqual(x2['s'], 45)
      self.assertEqual(x2['fg'], 'sdf')
      x2 = action('bot', 'get')
      print(x2)
      self.assertEqual(x2[1]['fg'], 'sdf')
if __name__ == '__main__':
    unittest.main()