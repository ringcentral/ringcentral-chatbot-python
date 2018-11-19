"""
bot auth
"""
import time
from .common import result
from .bot import Bot

def botAuth(event):
  bot = Bot()
  bot.auth(event.queryStringParameters.code)
  bot.renewWebHooks(event)
  # todo inject user custom hook here
  return result('Bot added')


def renewBot (event):
  """
  for self call renewbot async
  """
  if event.wait:
    time.sleep(event.wait)

  bot = Bot()
  bot.id = event.botId
  bot.token = event.token
  bot.writeToDb()
  bot.renewWebHooks(event)
  return result('Bot renew done')
