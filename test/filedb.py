import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from core.filedb import action

class TestStringMethods(unittest.TestCase):

    def test_basic(self):
      x = action('bot', 'write', {'s': 's', 'id': 'xss', 'dgfdf': [
        'sdfs', 'sdfsd'
      ]})
      self.assertEqual(x, 'x')

if __name__ == '__main__':
    unittest.main()