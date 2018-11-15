
import os
from ringcentral import SDK
from urllib.parse import parse_qs
import logging
from core.db import dbAction

class Bot:

  @classmethod
  def getBot(self, id):
    return dbAction('bot', 'get', {
      'id': id
    })

  @classmethod
  def removeBot(self, id):
    return dbAction('bot', 'remove', {
      'id': id
    })

  eventFilters: [
    '/restapi/v1.0/glip/posts',
    '/restapi/v1.0/glip/groups'
  ]

  id: ''

  def __init__(self, eventFilters, token, id):
    self.rcsdk = SDK(os.environ['BOT_CLIENT_ID'],os.environ['BOT_CLIENT_SECRET'],os.environ['RINGCENTRAL_ENV'])
    self.platform = self.rcsdk.platform()
    if eventFilters:
      self.eventFilters = eventFilters
    if token:
      self.token = token
    if id:
      self.id = id

  def writeTodb(self, item):
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
    redirect_url = os.environ['REDIRECT_HOST']+'/bot/oauth_prod'
    self.platform.login(code=code, redirect_uri=redirect_url)
    print('data from platform:')
    self.token = self.platform.auth().data()
    self.id = self.token.owner_id
    self.writeTodb()

  def renewWebHooks(event):

  def setupWebhook(event):

