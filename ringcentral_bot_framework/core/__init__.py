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
from .flask_request_parser import flaskRequestParser
import pydash as _

def frameworkInit(config, extensions = None):
  '''
  init bot framwork from config object and extensions array
  '''
  extensions = extensions or _.get(config, 'extensions') or []
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
    @staticmethod
    def Bot():
      return BotClass

    @staticmethod
    def User():
      return UserClass

    @staticmethod
    def dbAction(tableName, action, data = None):
      """db action
      * make sure it it stateless,
      * in every action, you should check database is ready or not, if not, init it first
      * check https://github.com/zxdong262/ringcentral-chatbot-python/blob/master/ringcentral_bot_framework/core/dynamodb.py or https://github.com/zxdong262/ringcentral-chatbot-python/blob/master/ringcentral_bot_framework/core/filedb.py as example
      * @param {String} tableName, user or bot, or other table you defined
      * @param {String} action, add, remove, update, get
      * @param {Object} data
      * for add, {'id': 'xxx', 'token': {...}, 'groups': {...}, 'data': {...}}
      * for remove, {'id': xxx} or {'ids': [...]}
      * for update, {'id': xxx, 'update': {...}}
      * for get, singleUser:{'id': xxx}, allUser: None, query: { 'key': 'xx', 'value': 'yy' }
      """
      return dbAction(tableName, action, data)

    @staticmethod
    def getBot(id):
      '''
      get bot data from database, init and return bot instance, if fails or not found will return False
      '''
      return getBot(id)

    @staticmethod
    def removeBot(id):
      '''
      remove bot data from database
      '''
      return removeBot(id)

    @staticmethod
    def getUser(id):
      '''
      get user data from database, init and return user instance, if fails or not found will return False
      '''
      return getUser(id)

    @staticmethod
    def removeUser(id):
      '''
      remove user data from database
      '''
      return removeUser(id)

    @staticmethod
    def botAuth(event):
      return botAuth(event)

    @staticmethod
    def renewBot(event):
      return renewBot(event)

    @staticmethod
    def botWebhook(event):
      return botWebhook(event)

    @staticmethod
    def dataView(event):
      return dataView(event)

    @staticmethod
    def userAuth(event):
      return userAuth(event)

    @staticmethod
    def userWebhook(event):
      return userWebhook(event)

    @staticmethod
    def router(event):
      '''
      process event and return result object:
      {
        'headers': dict,
        'body': dict,
        'statusCode': number
      }
      '''
      for extension in extensions:
        if hasattr(extension, 'route') and _.predicates.is_function(extension.route):
          res = extension.route(event, BotFrameWork)
          if not res is None:
            return res
      return router(event)

    @staticmethod
    def flaskRequestParser(request, action):
      '''
      parse flask request to event format:
      {
        'pathParameters': {
          'action': string
        },
        'queryStringParameters': dict,
        'body': dict,
        'headers': dict
      }
      '''
      return flaskRequestParser(request, action)

  return BotFrameWork

