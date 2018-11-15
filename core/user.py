
from os import environ
from ringcentral import SDK
from urllib.parse import parse_qs, urlencode
from core.db import dbAction
from core.common import debug, subscribeInterval

try:
  RINGCENTRAL_USER_CLIENT_ID = environ['RINGCENTRAL_USER_CLIENT_ID']
  RINGCENTRAL_USER_CLIENT_SECRET = environ['RINGCENTRAL_USER_CLIENT_SECRET']
  RINGCENTRAL_SERVER = environ['RINGCENTRAL_SERVER']
  RINGCENTRAL_BOT_SERVER = environ['RINGCENTRAL_USER_SERVER']

except:
  debug('load env error')

class User:

  @classmethod
  def getUser(self, id):
    return dbAction('user', 'get', {
      'id': id
    })

  @classmethod
  def removeUser(self, id):
    return dbAction('user', 'remove', {
      'id': id
    })

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
    except:
      self.removeUser(self.id)
      debug('refresh token has expired')
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
    except:
      # todo check sub-406 error and retry
      debug('setupWebhook error')

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

    except:
      debug('renewWebHooks error')

  def delSubscription (self, id):
    debug('del bot sub id:', id)
    try:
      self.platform.delete('/subscription/' + id)
    except:
      debug('delSubscription error')

  def removeGroup(self, id):
    self.groups.pop(id, None)
    self.writeToDb(False)

  def addGroup (self, groupId, botId):
    hasNoGroup = self.groups.keys().length == 0
    self.groups[groupId] = botId
    self.writeToDb()
    if hasNoGroup:
      self.setupWebhook()

  def validate (self):
    try:
      self.platform.get('/account/~/extension/~')
      return True
    except:
      debug('User validate error')
      return self.refresh()