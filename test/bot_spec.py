import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from ringcentral_bot_framework import frameworkInit
import default_conf as conf
framework = frameworkInit(conf)

action = framework.dbAction
DBNAME = 'filedb'
Bot = framework.Bot()
getBot = framework.getBot

class TestBot(unittest.TestCase):

  def test_basic_bot(self):
    print('running bot basic test')
    self.assertEqual(DBNAME, 'filedb')
    bot = Bot()
    self.assertEqual(bot.id, '')
    self.assertEqual(bot.token, {})
    self.assertEqual(bot.data, {})
    bot.id = 'u1'
    bot.token = {
      'id': 'u1',
      'f': 'sdf',
      'g': 54
    }
    bot.data = {
      'sdfsdf': 'sdfd'
    }
    bot.writeToDb({
      'id': bot.id,
      'data': bot.data,
      'token': bot.token
    })
    bot2 = getBot(bot.id)
    self.assertEqual(bot2.id, bot.id)
    self.assertEqual(bot.token, bot2.token)
    self.assertEqual(bot.data, bot2.data)

if __name__ == '__main__':
    unittest.main()