"""
bot auth
"""
from .common import result
from .bot import Bot
from pydash.predicates import is_string
from pydash import get
from .db import dbAction
from .config import configAll as conf

def botAuth(event):
  bot = Bot()
  code = get(event, 'queryStringParameters.code')
  if is_string(code):
    bot.auth(code)
  else:
    bot.authPrivateBot(event['body'])

  bot.renewWebHooks(event)
  conf.botAuthAction(bot, dbAction)
  return result('Bot added')

