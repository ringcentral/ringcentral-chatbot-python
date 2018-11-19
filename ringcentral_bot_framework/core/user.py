
from os import environ
from ringcentral import SDK
from urllib.parse import parse_qs, urlencode
from .db import dbAction
from .common import printError, debug, subscribeInterval

try:
  RINGCENTRAL_USER_CLIENT_ID = environ['RINGCENTRAL_USER_CLIENT_ID']
  RINGCENTRAL_USER_CLIENT_SECRET = environ['RINGCENTRAL_USER_CLIENT_SECRET']
  RINGCENTRAL_SERVER = environ['RINGCENTRAL_SERVER']
  RINGCENTRAL_BOT_SERVER = environ['RINGCENTRAL_BOT_SERVER']

except Exception as e:
  printError(e, 'load env')

class User:

  eventFilters: [
    '/restapi/v1.0/account/~/extension/~/message-store',
    subscribeInterval()
  ]

  id: ''
  groups: {}

  def __init__(self, eventFilters=False, token=False, id=False):
    self.rcsdk = SDK(
      RINGCENTRAL_USER_CLIENT_ID,
      RINGCENTRAL_USER_CLIENT_SECRET,
      RINGCENTRAL_SERVER
    )
    self.platform = self.rcsdk.platform()
    if eventFilters:
      self.eventFilters = eventFilters
    if token:
      self.token = token
      self.platform._auth.set_data(token)
    if id:
      self.id = id

  def writeToDb(self, item = False):
    if item:
      dbAction('bot', 'add', item)
    else:
      dbAction('bot', 'update', {
        'id': self.id,
        'group': self.groups,
        'update': {
          'token': self.token
        }
      })

  def getAuthUri (self, groupId, botId):
    redirect_url = RINGCENTRAL_BOT_SERVER + '/user-oauth'
    query = urlencode({
      'response_type': 'code',
      'redirect_uri': redirect_url,
      'client_id': RINGCENTRAL_USER_CLIENT_ID,
      'state': groupId + ',' + botId,
      'brand_id': '',
      'display': '',
      'prompt': '',
      'localeId': '',
      'ui_locales': '',
      'ui_options': ''
    })
    return f'{RINGCENTRAL_SERVER}/restapi/oauth/authorize?{query}'

  def auth(self, code):
    redirect_url = RINGCENTRAL_BOT_SERVER +'/bot-oauth'
    self.platform.login(code=code, redirect_uri=redirect_url)
    self.token = self.platform.auth().data()
    self.id = self.token.owner_id
    self.writeToDb(False)

  def refresh (self):
    try:
      self.platform.refresh()
      self.token = self.platform.auth().data()
      self.writeToDb(False)
      return True
    except Exception as e:
      printError(e, 'refrefresh token has expired')
      removeUser(self.id)
      return False

  def setupWebhook(self, event = False):
    try:
     self.platform.post('/subscription', {
        'eventFilters': self.eventFilters,
        'expiresIn': 1799,
        'deliveryMode': {
          'transportType': 'WebHook',
          'address': RINGCENTRAL_BOT_SERVER + '/bot-webhook'
        }
      })
    except Exception as e:
      printError(e, 'setupWebhook')

  def renewWebHooks(self, event):
    try:
      r = self.platform.get('/subscription')
      r = r.json()
      filtered = filter(
        lambda x: x.deliveryMode.address == RINGCENTRAL_BOT_SERVER +'/bot-webhook',
        r
      )
      debug(
        'user subs list',
        ','.join(map(lambda g: g.id, filtered))
      )
      self.setupWebhook(event)
      for sub in filtered:
        self.delSubscription(sub.id)

    except Exception as e:
      printError(e, 'renewWebHooks')

  def delSubscription (self, id):
    debug('del user sub id:', id)
    try:
      self.platform.delete('/subscription/' + id)
    except Exception as e:
      printError(e, 'delSubscription')

  def removeGroup(self, id):
    self.groups.pop(id, None)
    self.writeToDb(False)

  def addGroup (self, groupId, botId):
    hasNoGroup = len(self.groups.keys()) == 0
    self.groups[groupId] = botId
    self.writeToDb()
    if hasNoGroup:
      self.setupWebhook()

  def validate (self):
    try:
      self.platform.get('/account/~/extension/~')
      return True
    except Exception as e:
      printError(e, 'validate')
      return self.refresh()


def getUser(id):
  userData = dbAction('user', 'get', {
    'id': id
  })
  if userData != False:
    return User(userData.id, userData.token)
  else:
    return False

def removeUser(id):
  return dbAction('user', 'remove', {
    'id': id
  })