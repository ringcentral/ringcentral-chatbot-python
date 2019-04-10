import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from ringcentral_bot_framework import frameworkInit
import default_conf as conf
framework = frameworkInit(conf)
DBNAME = 'dynamodb'
action = framework.dbAction

class TestDynamodbMethods(unittest.TestCase):

  def test_basic_dynamodb(self):
    print('running dynamodb test')
    self.assertEqual(DBNAME, 'dynamodb')
    x = action('bot', 'add', {
      'id': 'xss2',
      'token': {
        'a': 'b',
        'b': 4
      }
    })
    self.assertEqual(x, 'add')
    x1 = action('bot', 'add', {
      'id': 'xss1',
      'token': {
        'a': 'a',
        'b': 1
      }
    })
    self.assertEqual(x1, 'add')
    x2 = action('bot', 'get', { 'id': 'xss1' })
    self.assertEqual(x2['id'], 'xss1')
    x2 = action('bot', 'update', { 'id': 'xss1', 'update': {
      'token': {'n': 45},
      'x': 'c',
      'data': {
        'dd': 'ff'
      }
    }})
    x2 = action('bot', 'get', { 'id': 'xss1'})
    self.assertEqual(x2['id'], 'xss1')
    self.assertEqual(x2['token']['n'], 45)
    self.assertEqual(x2['data']['dd'], 'ff')
    x2 = action('bot', 'get')
    self.assertEqual(x2[0]['token']['n'], 45)
    action('bot', 'add', {
      'id': 'xss3',
      'x': 'c'
    })
    x2 = action('bot', 'get', { 'key': 'x', 'value': 'c' })
    self.assertEqual(x2[0]['x'], 'c')
    self.assertEqual(len(x2), 2)
if __name__ == '__main__':
    unittest.main()