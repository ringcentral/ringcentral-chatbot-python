
from os import environ
from ringcentral import SDK
from .db import dbAction
from .common import debug, printError
from pydash.predicates import is_dict
from pydash.objects import omit
import json
from .config import configAll as conf

try:
  RINGCENTRAL_BOT_CLIENT_ID = environ['RINGCENTRAL_BOT_CLIENT_ID']
  RINGCENTRAL_BOT_CLIENT_SECRET = environ['RINGCENTRAL_BOT_CLIENT_SECRET']
  RINGCENTRAL_SERVER = environ['RINGCENTRAL_SERVER']
  RINGCENTRAL_BOT_SERVER = environ['RINGCENTRAL_BOT_SERVER']

except Exception as e:
  printError(e, 'load env')

class Bot:

  def __init__(
    self,
    id=None,
    token=None,
    data=None
  ):
    self.rcsdk = SDK(
      RINGCENTRAL_BOT_CLIENT_ID,
      RINGCENTRAL_BOT_CLIENT_SECRET,
      RINGCENTRAL_SERVER
    )
    self.platform = self.rcsdk.platform()
    if not token is None:
      self.token = token
      self.platform._auth.set_data(token)
    if not data is None:
      self.data = data
    if not id is None:
      self.id = id

  eventFilters = conf.botFilters()
  id = ''
  token = {}
  data = {}

  def writeToDb(self, item=False):
    if is_dict(item):
      dbAction('bot', 'add', item)
    else:
      dbAction('bot', 'update', {
        'id': self.id,
        'update': {
          'token': self.token
        },
        'data': self.data
      })

  def auth(self, code):
    redirect_url = RINGCENTRAL_BOT_SERVER +'/bot-oauth'
    self.platform.login(code=code, redirect_uri=redirect_url)
    self.token = self.platform.auth().data()
    info = self.validate(True)
    txt = json.loads(info.text())
    self.token['name'] = txt['name']
    self.id = self.token['owner_id']
    self.writeToDb({
      'id': self.id,
      'token': self.token,
      'data': self.data
    })

  def authPrivateBot(self, _token):
    access_token = _token['access_token'][0]
    token = {
      'token_type': 'bearer',
      'access_token': access_token,
      'expires_in': 2147483647,
      'expire_time': 3690554048.892673,
      'refresh_token': '',
      'refresh_token_expires_in': 0,
      'refresh_token_expire_time': 0,
    }
    self.platform._auth.set_data(token)
    info = self.validate(True)
    txt = json.loads(info.text())
    token['owner_id'] = str(txt['id'])
    token['name'] = txt['name']
    token['scope'] = ' '.join(
      list(
        map(lambda x: x['featureName'], txt['serviceFeatures'])
      )
    )
    self.platform._auth.set_data(token)
    self.token = token
    self.id = token['owner_id']
    self.writeToDb({
      'id': self.id,
      'token': self.token,
      'data': self.data
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

  def renewWebHooks(self, event, removeOnly = False):
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
      if not removeOnly:
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

  def validate (self, returnData=False):
    try:
      res = self.platform.get('/account/~/extension/~')
      return res if returnData else True
    except Exception as e:
      errStr = str(e)
      print(errStr, '----')
      if 'OAU-232' in errStr or 'CMN-405' in errStr:
        removeBot(self.id)
      return False

  def destroy(self):
    self.renewWebHooks(None, True)
    removeBot(self.id)

def getBot(id):
  if not id:
    return False
  botData = dbAction('bot', 'get', {
    'id': id
  })
  if is_dict(botData):
    return Bot(
      botData['id'],
      botData['token'],
      botData['data']
    )
  else:
    return False

def removeBot(id):
    return dbAction('bot', 'remove', {
      'id': id
    })