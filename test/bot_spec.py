import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from ringcentral_bot_framework.core.db import dbAction as action, DBNAME
from ringcentral_bot_framework.core.bot import Bot, getBot

class TestBot(unittest.TestCase):

  def test_basic_bot(self):
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