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
from .route import initRouter

def frameworkInit(config, extensions = []):
  '''
  init bot framwork from config object and extensions array
  '''
  conf = initConfig(config)
  dbAction = initDBAction(conf)
  BotClass, getBot, removeBot = initBotClass(conf, dbAction)
  UserClass, getUser, removeUser = initUserClass(conf, dbAction)
  botAuth, renewBot = initBotAuthHandler(conf, BotClass, dbAction)
  botWebhook = initBotWebhook(
    conf, dbAction, BotClass, UserClass, getBot, getUser, extensions
  )
  dataView = initDataView(conf, dbAction)
  userAuth = initUserAuth(
    conf, BotClass, getBot, UserClass, dbAction
  )
  userWebhook = initUserWebhook(
    conf, BotClass, getBot, UserClass, getUser, dbAction
  )

  routes = {
    'bot-oauth': botAuth,
    'renew-bot': renewBot,
    'user-oauth': userAuth,
    'bot-webhook': botWebhook,
    'user-webhook': userWebhook,
    'data': dataView
  }

  router = initRouter(routes)

  class BotFrameWork:
    Bot = BotClass,
    User = UserClass

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

    @staticmethod
    def router(*args, **kwargs):
      return router(*args, **kwargs)

  return BotFrameWork

