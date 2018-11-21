
from os import environ
from ringcentral import SDK
from .db import dbAction
from .common import debug, printError
from pydash.predicates import is_dict
import json

try:
  RINGCENTRAL_BOT_CLIENT_ID = environ['RINGCENTRAL_BOT_CLIENT_ID']
  RINGCENTRAL_BOT_CLIENT_SECRET = environ['RINGCENTRAL_BOT_CLIENT_SECRET']
  RINGCENTRAL_SERVER = environ['RINGCENTRAL_SERVER']
  RINGCENTRAL_BOT_SERVER = environ['RINGCENTRAL_BOT_SERVER']

except Exception as e:
  printError(e, 'load env')

class Bot:

  def __init__(self, id=False, token=False, eventFilters=False):
    self.rcsdk = SDK(
      RINGCENTRAL_BOT_CLIENT_ID,
      RINGCENTRAL_BOT_CLIENT_SECRET,
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

  eventFilters = [
    '/restapi/v1.0/glip/posts',
    '/restapi/v1.0/glip/groups'
  ]

  id = ''

  def writeToDb(self, item=False):
    if is_dict(item):
      dbAction('bot', 'add', item)
    else:
      dbAction('bot', 'update', {
        'id': self.id,
        'update': {
          'token': self.token
        }
      })

  def auth(self, code):
    redirect_url = RINGCENTRAL_BOT_SERVER +'/bot-oauth'
    self.platform.login(code=code, redirect_uri=redirect_url)
    self.token = self.platform.auth().data()
    self.id = self.token['owner_id']
    self.writeToDb({
      'id': self.id,
      'token': self.token
    })

  def setupWebhook(self, event):
    try:
     self.platform.post('/subscription', {
        'eventFilters': self.eventFilters,
        'expiresIn': 500000000,
        'deliveryMode': {
          'transportType': 'WebHook',
          'address': RINGCENTRAL_BOT_SERVER + '/bot-webhook'
        }
      })
    except Exception as e:
      # todo check sub-406 error and retry
      printError(e, 'setupWebhook')

  def renewWebHooks(self, event):
    try:
      r = self.platform.get('/subscription')
      r = json.loads(r.text())['records']
      filtered = list(filter(
        lambda x: x['deliveryMode']['address'] == RINGCENTRAL_BOT_SERVER + '/bot-webhook',
        r
      ))
      debug(
        'bot subs list',
        ','.join(list(map(lambda g: g['id'], filtered)))
      )
      self.setupWebhook(event)
      for sub in filtered:
        self.delSubscription(sub['id'])

    except Exception as e:
      printError(e, 'renewWebHooks')

  def delSubscription (self, id):
    debug('del bot sub id:', id)
    try:
      self.platform.delete('/subscription/' + id)
    except Exception as e:
      printError(e, 'delSubscription')

  def sendMessage (self, groupId, messageObj):
    try:
      url = f'/restapi/v1.0/glip/groups/{groupId}/posts'
      headers = {
        'Authorization': 'bearer ' + self.token['access_token']
      }
      self.platform.post(
        url,
        messageObj,
        headers=headers
      )
    except Exception as e:
      printError(e, 'sendMessage')

  def validate (self):
    try:
      self.platform.get('/account/~/extension/~')
      return True
    except Exception as e:
      errStr = str(e)
      if 'OAU-232' in errStr or 'CMN-405' in errStr:
        removeBot(self.id)
      return False

def getBot(id):
  if not id:
    return False
  botData = dbAction('bot', 'get', {
    'id': id
  })
  if is_dict(botData):
    return Bot(botData['id'], botData['token'])
  else:
    return False

def removeBot(id):
    return dbAction('bot', 'remove', {
      'id': id
    })