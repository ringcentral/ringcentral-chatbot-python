'''
framework entry
'''
from .bot import initBotClass
from .db import initDBAction
from .user import initUserClass
from .bot_oauth import initBotAuthHandler
from .user_oauth import initUserAuth
from .bot_webhook import initBotWebhook
from .config import initConfig
from .data import initDataView
from .user_webhook import initUserWebhook

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
    conf, dbAction, Bot, User, getBot, getUser, extensions
  )
  dataView = initDataView(conf, dbAction)
  userAuth = initUserAuth(
    conf, Bot, getBot, User, dbAction
  )
  userWebhook = initUserWebhook(
    conf, Bot, getBot, User, getUser, dbAction
  )

  class BotFrameWork:
    Bot = Bot
    User = User

    @staticmethod
    def dbAction(*args, **kwargs):
      return dbAction(*args, **kwargs)

    @staticmethod
    def getBot(*args, **kwargs):
      return getBot(*args, **kwargs)

    @staticmethod
    def removeBot(*args, **kwargs):
      return removeBot(*args, **kwargs)

    @staticmethod
    def getUser(*args, **kwargs):
      return getUser(*args, **kwargs)

    @staticmethod
    def removeUser(*args, **kwargs):
      return removeUser(*args, **kwargs)

    @staticmethod
    def botAuth(*args, **kwargs):
      return botAuth(*args, **kwargs)

    @staticmethod
    def renewBot(*args, **kwargs):
      return renewBot(*args, **kwargs)

    @staticmethod
    def botWebhook(*args, **kwargs):
      return botWebhook(*args, **kwargs)

    @staticmethod
    def dataView(*args, **kwargs):
      return dataView(*args, **kwargs)

    @staticmethod
    def userAuth(*args, **kwargs):
      return userAuth(*args, **kwargs)

    @staticmethod
    def userWebhook(*args, **kwargs):
      return userWebhook(*args, **kwargs)

  return BotFrameWork

