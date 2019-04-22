"""
default config module
could write config.py to override all the bot behavior
"""

__name__ = 'defaultConfig'
__package__ = 'ringcentral_bot_framework.core'

import copy

'''
use extensions

example:

import ringcentral_bot_framework_extension_world_time as wt
extensions = [wt]

'''
extensions = []

def botJoinPrivateChatAction(bot, groupId, user, dbAction):
  """
  bot join private chat event handler
  bot could send some welcome message or help, or something else
  """
  bot.sendMessage(
    groupId,
    {
      'text': f'Hello, I am a chatbot. Please reply "![:Person]({bot.id})" if you want to talk to me.'
    }
  )

def botGotPostAddAction(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction,
  handledByExtension,
  event
):
  """
  bot got group chat message: text
  bot could send some response
  """
  if handledByExtension:
    return

  if f'![:Person]({bot.id})' in text:
    bot.sendMessage(
      groupId,
      {
        'text': f'![:Person]({creatorId}), Hello, you just posted "{text}"'
      }
    )

def botGroupLeftAction(
  bot,
  message,
  dbAction
):
  """
  got message that bot has left chat group
  could do some clean up work here
  default: remove group id ref in all user database
  """
  users = dbAction('user', 'get')
  for user in users:
    id = user['id']
    groups = user['groups']
    keys = groups.keys()
    ngroups = copy.deepcopy(groups)
    for groupId in keys:
      if groups[groupId] == bot.id:
        ngroups.pop(groupId, None)
    dbAction('user', 'update', {
      'id': id,
      'update': {
        'groups': ngroups
      }
    })


def botDeleteAction(bot, message, dbAction):
  """
  got message that bot has beed deleted
  could do some clean up work here
  default: delete bot from database
  """
  bot.destroy()

def botAuthAction(bot, dbAction):
  '''
  After bot auth success,
  can do some bot actions
  default: do nothing
  '''
  return

def defaultEventHandler(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction,
  handledByExtension,
  event
):
  """
  default event handler, for event not match any above
  """
  return

def userAuthSuccessAction(bot, groupId, userId, dbAction):
  """
  user auth bot app to access user data success,
  bot would do something
  default: send login success message to chatgroup
  if you only have bot app, it is not needed
  """
  bot.sendMessage(groupId, {
    'text': f'![:Person]({userId}), you have successfully authorized me to access your RingCentral data!'
  })

def userAddGroupInfoAction(bot, user, groupId, dbAction):
  """
  user add group and bot connect info,
  bot or user could do something about it,
  default: do nothing
  if you only have bot app, it is not needed
  """
  return

def userAuthSuccessHtml(user, conf):
  """
  user auth success, would see this html from browser
  if you only have bot app, it is not needed
  """
  return '<div style="text-align: center;font-size: 20px;border: 5px solid #08c;padding: 30px;">You have authorized the bot to access your RingCentral data! Please close this page and get back to Glip</div>'

def userEventAction(
  user,
  eventType,
  event,
  getBot,
  dbAction
):
  """
  bot got subscribed user event,
  do something about it
  default: post to chatgroup about the event
  if you only have bot app, it is not needed
  """
  groups = user.groups
  keys = groups.keys()
  for groupId in keys:
    botId = groups[groupId]
    bot = getBot(botId)
    if bot != False and eventType != 'PostAdded':
      bot.sendMessage(groupId, {
        'text': f'![:Person]({user.id}), got event "{eventType}"'
      })

def botFilters():
  '''
  customize bot filters to subscribe
  '''
  return [
    '/restapi/v1.0/glip/posts',
    '/restapi/v1.0/glip/groups',
    '/restapi/v1.0/account/~/extension/~'
  ]

def userFilters():
  '''
  customize user filters to subscribe
  '''
  return [
    '/restapi/v1.0/account/~/extension/~/message-store'
  ]

def dbTables():
  '''
  db tables to init
  '''
  return [
    {
      'name': 'bot',
      'schemas': [
        {
          'name': 'id',
          'type': 'string',
          'primary': True
        },
        {
          'name': 'token',
          'type': 'json'
        },
        {
          'name': 'data',
          'type': 'json'
        }
      ]
    },
    {
      'name': 'user',
      'schemas': [
        {
          'name': 'id',
          'type': 'string',
          'primary': True
        },
        {
          'name': 'token',
          'type': 'json'
        },
        {
          'name': 'groups',
          'type': 'json'
        },
        {
          'name': 'data',
          'type': 'json'
        }
      ]
    }
  ]

def dbWrapper(tableName, action, data = None):
  """custom db action wrapper
  * set DB_TYPE=custom in .env to activate
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

  # todo prepare/check database
  # prepareDB()
  try:
    id = None
    if 'id' in data:
      id = data['id']

    if action == 'add':
      # todo
      print(id)
      return 'added'

    elif action == 'remove':
      # todo
      return 'removed'

    elif action == 'update':
      # todo
      return 'updated'

    elif action == 'get':
      # todo
      if not id is None:
        return {}
      else:
        return [{}]

  except Exception as e:
    print(e)
    return False

def dbName():
  '''
  return db name
  * set DB_TYPE=custom in .env to activate
  '''
  return 'custom'