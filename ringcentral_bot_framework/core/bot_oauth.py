"""
bot auth
"""
import time
from .common import result
from .bot import Bot
from pydash.predicates import is_number
from pydash import get
from .db import dbAction
from .config import configAll as conf

def botAuth(event):
  bot = Bot()
  bot.auth(get(event, 'queryStringParameters.code'))
  bot.renewWebHooks(event)
  conf.botAuthAction(bot, dbAction)
  return result('Bot added')

def renewBot (event):
  """
  for self call renewbot async
  """
  if is_number(event['wait']):
    time.sleep(event['wait'])

  bot = Bot()
  bot.id = event.id
  event.botId
  bot.token = event.token
  bot.writeToDb()
  bot.renewWebHooks(event)
  return result('Bot renew done')
