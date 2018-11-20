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
from pydash import get
from pydash.predicates import is_dict
import json

routes = {
  'bot-oauth': botAuth,
  'user-oauth': userAuth,
  'bot-webhook': botWebhook,
  'user-webhook': userWebhook
}

def router(event):
  debug('got event', event)
  action = get(event, 'pathParameters.action')
  handler = defaultEventHandler
  debug('action=====', action)
  if not is_dict(event['body']):
    try:
      event['body'] = json.loads(event['body'] or '{}')
    except:
      pass
  try:
    handler = routes[action]
  except:
    pass
  return handler(event)