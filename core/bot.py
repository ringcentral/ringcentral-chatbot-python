
import os
from ringcentral import SDK
from urllib.parse import parse_qs
import logging

class Bot:

  eventFilters: [
    '/restapi/v1.0/glip/posts',
    '/restapi/v1.0/glip/groups'
  ]

  def __init__(self, eventFilters, token):
    self.rcsdk = SDK(os.environ['BOT_CLIENT_ID'],os.environ['BOT_CLIENT_SECRET'],os.environ['RINGCENTRAL_ENV'])
    self.platform = self.rcsdk.platform()
    if eventFilters:
      self.eventFilters = eventFilters
    if token:
      self.token = token

  def writeTodb(self):


  def auth(self, code):
    redirect_url = os.environ['REDIRECT_HOST']+'/bot/oauth_prod'
    self.platform.login(code=code, redirect_uri=redirect_url)
    print('data from platform:')
    self.token = self.platform.auth().data())


