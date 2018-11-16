import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from core.filedb import action

class TestStringMethods(unittest.TestCase):

    def test_basic(self):
      x = action('bot', 'write', {'s': 's', 'id': 'xss', 'dgfdf': [
        'sdfs', 'sdfsd'
      ]})
      self.assertEqual(x, 'write')
      x1 = action('bot', 'write', {'s': 's', 'id': 'xss1', 'dgfdf': [
        'sdfs', 'sdfsd'
      ]})
      self.assertEqual(x1, 'write')
      x2 = action('bot', 'get', { 'id': 'xss1'})
      self.assertEqual(x2.id, 'xss1')
if __name__ == '__main__':
    unittest.main()