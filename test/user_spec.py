import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from ringcentral_bot_framework import frameworkInit
import default_conf as conf
framework = frameworkInit(conf)
DBNAME = 'filedb'
action = framework.dbAction
getUser = framework.getUser
User = framework.User()

class TestUser(unittest.TestCase):

  def test_basic_user(self):
    print('running user basic test')
    self.assertEqual(DBNAME, 'filedb')
    user = User()
    self.assertEqual(user.id, '')
    self.assertEqual(user.token, {})
    self.assertEqual(user.groups, {})
    self.assertEqual(user.data, {})
    user.id = 'u1'
    user.token = {
      'id': 'u1',
      'f': 'sdf',
      'g': 54
    }
    user.groups = {
      'df': 'sdf'
    }
    user.data = {
      'sdfsdf': 'sdfd'
    }
    user.writeToDb({
      'id': user.id,
      'groups': user.groups,
      'data': user.data,
      'token': user.token
    })
    user2 = getUser(user.id)
    self.assertEqual(user2.id, user.id)
    self.assertEqual(user.token, user2.token)
    self.assertEqual(user.groups, user2.groups)
    self.assertEqual(user.data, user2.data)

if __name__ == '__main__':
    unittest.main()