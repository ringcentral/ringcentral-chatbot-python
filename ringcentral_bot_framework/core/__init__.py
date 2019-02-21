'''
framework entry
'''
from .bot import initBotClass
from .db import initDBAction
from .user import initUserClass
from .bot_oauth import initBotAuthHandler
from .bot_webhook import initBotWebhook
from .config import initConfig
from .data import initDataView

def frameworkInit(config, extensions = []):
  '''
  init bot framwork from config object and extensions array
  '''
  conf = initConfig(config)
  dbAction = initDBAction(conf)
  Bot, getBot, removeBot = initBotClass(conf, dbAction)
  User, getUser, removeUser = initUserClass(conf, dbAction)
  botAuth, renewBot = initBotAuthHandler(conf, Bot, dbAction)
  botWebhook = initBotWebhook(
    conf, dbAction, Bot, User, getBot, getUser
  )
  dataView = initDataView(conf, dbAction)

  class BotFrameWork:
    dbAction = dbAction
    Bot = Bot
    getBot =getBot
    removeBot = removeBot
    User = User
    getUser = getUser
    removeUser = removeUser
    botAuth = botAuth
    renewBot = renewBot
    botWebhook = botWebhook
    dataView = dataView

  return BotFrameWork()

