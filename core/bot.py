
from os import environ
from ringcentral import SDK
from urllib.parse import parse_qs
import logging
from core.db import dbAction
from core.common import debug

try:
  RINGCENTRAL_BOT_CLIENT_ID = environ['RINGCENTRAL_BOT_CLIENT_ID']
  RINGCENTRAL_BOT_CLIENT_SECRET = environ['RINGCENTRAL_BOT_CLIENT_SECRET']
  RINGCENTRAL_SERVER = environ['RINGCENTRAL_SERVER']
  RINGCENTRAL_BOT_SERVER = environ['RINGCENTRAL_BOT_SERVER']

except:
  debug('load env error')

class Bot:

  eventFilters: [
    '/restapi/v1.0/glip/posts',
    '/restapi/v1.0/glip/groups'
  ]

  id: ''

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
      #todo platform set token
    if id:
      self.id = id

  def writeToDb(self, item=False):
    if item:
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
    self.id = self.token.owner_id
    self.writeToDb(False)

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
    except:
      # todo check sub-406 error and retry
      debug('setupWebhook error')

  def renewWebHooks(self, event):
    try:
      r = self.platform.get('/subscription')
      r = r.json()
      filtered = filter(
        lambda r: r.deliveryMode.address == RINGCENTRAL_BOT_SERVER +'/bot-webhook',
        r
      )
      debug(
        'bot subs list',
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

  def sendMessage (self, groupId, messageObj):
    try:
      self.platform.post(
        '/glip/groups/{groupId}/posts',
        messageObj
      )
    except:
      debug('sendMessage error')

  def validate (self):
    try:
      self.platform.get('/account/~/extension/~')
      return True
    except:
      removeBot(self.id)
      # todo: 'OAU-232' || 'CMN-405' error triggers remove
      return False

def getBot(id):
    botData = dbAction('bot', 'get', {
      'id': id
    })
    if botData != False:
      return Bot(botData.id, botData.token)
    else:
      return False

def removeBot(id):
    return dbAction('bot', 'remove', {
      'id': id
    })