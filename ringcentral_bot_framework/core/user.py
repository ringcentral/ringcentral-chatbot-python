
from os import environ
from ringcentral_client import RestClient
from urllib.parse import urlencode
from pydash.predicates import is_dict
from pydash.objects import omit
import json
from .common import printError, debug, subscribeInterval

RINGCENTRAL_SERVER = environ['RINGCENTRAL_SERVER']
RINGCENTRAL_BOT_SERVER = environ['RINGCENTRAL_BOT_SERVER']
RINGCENTRAL_USER_CLIENT_ID = ''
RINGCENTRAL_USER_CLIENT_SECRET = ''

try:
  RINGCENTRAL_USER_CLIENT_ID = environ['RINGCENTRAL_USER_CLIENT_ID']
  RINGCENTRAL_USER_CLIENT_SECRET = environ['RINGCENTRAL_USER_CLIENT_SECRET']

except Exception as e:
  printError(e, 'user load env')

def initUserClass(conf, dbAction):
  class User:

    def __init__(
      self,
      id=None,
      token=None,
      groups=None,
      data=None
    ):
      self.rc = RestClient(
        RINGCENTRAL_USER_CLIENT_ID,
        RINGCENTRAL_USER_CLIENT_SECRET,
        RINGCENTRAL_SERVER
      )
      self.platform = self.rc
      if not token is None:
        self.token = token
        self.rc.token = token
      if not groups is None:
        self.groups = groups
      if not data is None:
        self.data = data
      if not id is None:
        self.id = id

    id = ''
    groups = {}
    data = {}
    token = {}
    eventFilters = conf.userFilters() + [subscribeInterval()]

    def writeToDb(self, item = False):
      if is_dict(item):
        dbAction('user', 'add', item)
      else:
        dbAction('user', 'update', {
          'id': self.id,
          'update': {
            'token': self.token,
            'groups': self.groups,
            'data': self.data
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
      redirect_url = RINGCENTRAL_BOT_SERVER +'/user-oauth'
      self.rc.authorize(auth_code=code, redirect_uri=redirect_url)
      self.token = self.rc.token
      self.id = self.token['owner_id']
      self.writeToDb({
        'id': self.id,
        'token': self.token,
        'groups': self.groups,
        'data': self.data
      })

    def refresh (self):
      try:
        self.rc.refresh()
        self.token = self.rc.token
        self.writeToDb(False)
        return True
      except Exception as e:
        printError(e, 'user refrefresh token has expired')
        removeUser(self.id)
        return False

    def setupWebhook(self, event=None):
      try:
        self.platform.post('/restapi/v1.0/subscription', {
          'eventFilters': self.eventFilters,
          'expiresIn': 1799,
          'deliveryMode': {
            'transportType': 'WebHook',
            'address': RINGCENTRAL_BOT_SERVER + '/user-webhook'
          }
        })
      except Exception as e:
        printError(e, 'user setupWebhook')

    def renewWebHooks(self, event=None):
      try:
        r = self.platform.get('/restapi/v1.0/subscription')
        r = json.loads(r.text)['records']
        filtered = list(filter(
          lambda x: x['deliveryMode']['address'] == RINGCENTRAL_BOT_SERVER + '/user-webhook',
          r
        ))
        debug(
          'user subs list',
          ','.join(list(map(lambda g: g['id'], filtered)))
        )
        self.setupWebhook(event)
        for sub in filtered:
          self.delSubscription(sub['id'])

      except Exception as e:
        printError(e, 'user renewWebHooks')

    def delSubscription (self, id):
      debug('del user sub id:', id)
      try:
        self.platform.delete('/restapi/v1.0/subscription/' + id)
      except Exception as e:
        printError(e, 'user delSubscription')

    def removeGroup(self, id):
      self.groups.pop(id, None)
      self.writeToDb(False)

    def addGroup (self, groupId, botId):
      hasNoGroup = len(self.groups.keys()) == 0
      self.groups[groupId] = botId
      self.writeToDb()
      if hasNoGroup:
        self.renewWebHooks()

    def validate (self):
      try:
        self.rc.get('/restapi/v1.0/account/~/extension/~')
        return True
      except Exception as e:
        printError(e, 'user validate')
        return self.refresh()


  def getUser(id):
    if RINGCENTRAL_USER_CLIENT_ID == '':
      return False
    userData = dbAction('user', 'get', {
      'id': id
    })
    if is_dict(userData):
      return User(
        userData['id'],
        userData['token'],
        userData['groups'],
        userData['data']
      )
    else:
      return False

  def removeUser(id):
    if RINGCENTRAL_USER_CLIENT_ID == '':
      return False
    return dbAction('user', 'remove', {
      'id': id
    })
  return User, getUser, removeUser