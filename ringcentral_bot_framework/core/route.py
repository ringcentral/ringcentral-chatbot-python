"""
route /{action} to different event handeler
/bot-oauth bot auth
/user-oauth user auth
/bot-webhook bot webhook
/user-webhook user webhook

extend or overide default route by set `routes` in config.py
"""

from .bot_oauth import botAuth
from .user_oauth import userAuth
from .bot_webhook import botWebhook
from .user_webhook import userWebhook
from .common import debug, defaultEventHandler

routes = {
  'bot-oauth': botAuth,
  'user-oauth': userAuth,
  'bot-webhook': botWebhook,
  'user-webhook': userWebhook
}

def router(event):
  debug('got event', event)
  action = event['pathParameters']['action']
  handler = defaultEventHandler
  print('action=====', action)
  try:
    handler = routes[action]
  except:
    pass
  return handler(event)