
from os import environ
from ringcentral_client import RestClient
from .common import debug, printError
from .self_run import selfTrigger
from pydash.predicates import is_dict
from pydash.objects import omit
import json

try:
  RINGCENTRAL_BOT_CLIENT_ID = environ['RINGCENTRAL_BOT_CLIENT_ID']
  RINGCENTRAL_BOT_CLIENT_SECRET = environ['RINGCENTRAL_BOT_CLIENT_SECRET']
  RINGCENTRAL_SERVER = environ['RINGCENTRAL_SERVER']
  RINGCENTRAL_BOT_SERVER = environ['RINGCENTRAL_BOT_SERVER']

except Exception as e:
  printError(e, 'load env')

def initBotClass(conf, dbAction):
  class Bot:

    def __init__(
      self,
      id=None,
      token=None,
      data=None
    ):
      self.rc = RestClient(
        RINGCENTRAL_BOT_CLIENT_ID,
        RINGCENTRAL_BOT_CLIENT_SECRET,
        RINGCENTRAL_SERVER
      )
      self.platform = self.rc
      if not token is None:
        self.token = token
        self.rc.token = token
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
      self.rc.authorize(auth_code=code, redirect_uri=redirect_url)
      self.token = self.rc.token
      info = self.validate(True)
      txt = json.loads(info.text)
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
      self.rc.token = token
      info = self.validate(True)
      txt = json.loads(info.text)
      token['owner_id'] = str(txt['id'])
      token['name'] = txt['name']
      token['scope'] = ' '.join(
        list(
          map(lambda x: x['featureName'], txt['serviceFeatures'])
        )
      )
      self.rc.token = token
      self.token = token
      self.id = token['owner_id']
      self.writeToDb({
        'id': self.id,
        'token': self.token,
        'data': self.data
      })

    def setupWebhook(self, event):
      try:
        self.rc.post('/restapi/v1.0/subscription', {
          'eventFilters': self.eventFilters,
          'expiresIn': 500000000,
          'deliveryMode': {
            'transportType': 'WebHook',
            'address': RINGCENTRAL_BOT_SERVER + '/bot-webhook'
          }
        })
      except Exception as e:
        debug(e)
        errStr = str(e)
        if 'OAU-232' in errStr or 'SUB-406' in errStr or 'Not allowed subscribe' in errStr:
          printError('bot subscribe fail, will do subscribe one minutes later')
          event['wait'] = 50
          event['botId'] = self.id
          event['token'] = self.token
          event['pathParameters']['action'] = 'renew-bot'
          selfTrigger(event, conf, dbAction, Bot)
        else:
          printError(e, 'setupWebhook')

    def renewWebHooks(self, event, removeOnly = False):
      try:
        r = self.rc.get('/restapi/v1.0/subscription')
        r = json.loads(r.text)['records']
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
        debug(e)
        errStr = str(e)
        if event is None:
          printError(e, 'renewWebHooks')
        elif 'OAU-232' in errStr or 'SUB-406' in errStr or 'Not allowed subscribe' in errStr:
          printError('bot subscribe fail, will do subscribe one minutes later')
          event['wait'] = 50
          event['botId'] = self.id
          event['token'] = self.token
          event['pathParameters']['action'] = 'renew-bot'
          selfTrigger(event, conf, dbAction, Bot)
        else:
          printError(e, 'renewWebHooks')

    def delSubscription (self, id):
      debug('del bot sub id:', id)
      try:
        self.rc.delete('/restapi/v1.0/subscription/' + id)
      except Exception as e:
        printError(e, 'delSubscription')

    def sendMessage (self, groupId, messageObj):
      try:
        url = f'/restapi/v1.0/glip/groups/{groupId}/posts'
        self.rc.post(
          url,
          messageObj
        )
      except Exception as e:
        printError(e, 'sendMessage')

    def rename (self, newName):
      return self.rc.put(
        '/restapi/v1.0/account/~/extension/~',
        {
          'contact': { 'firstName': newName }
        }
      )

    def setAvatar (self, data, name):
      files = {'image': (name, data, 'image/png')}
      return self.rc.put(
        '/restapi/v1.0/account/~/extension/~/profile-image',
        files = files
      )

    def validate (self, returnData=False):
      try:
        res = self.platform.get('/restapi/v1.0/account/~/extension/~')
        return res if returnData else True
      except Exception as e:
        errStr = str(e)
        printError(errStr)
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

  return Bot, getBot, removeBot
