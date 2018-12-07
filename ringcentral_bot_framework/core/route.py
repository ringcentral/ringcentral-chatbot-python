"""
route /{action} to different event handeler
/bot-oauth bot auth
/user-oauth user auth
/bot-webhook bot webhook
/user-webhook user webhook

extend or overide default route by set `routes` in config.py
"""

from urllib.parse import parse_qs, urlencode
from .bot_oauth import botAuth
from .user_oauth import userAuth
from .bot_webhook import botWebhook
from .user_webhook import userWebhook
from .data import dataView
from .common import debug, defaultEventHandler
from pydash import get
from pydash.predicates import is_dict
import json

routes = {
  'bot-oauth': botAuth,
  'user-oauth': userAuth,
  'bot-webhook': botWebhook,
  'user-webhook': userWebhook,
  'data': dataView
}

def router(event):
  debug('got event', event)
  action = get(event, 'pathParameters.action')
  handler = defaultEventHandler
  debug('action=====', action)
  body = get(event, 'body')
  if not is_dict(body):
    if 'application/x-www-form-urlencoded' in get(event, 'headers.Content-Type'):
      event['body'] = parse_qs(body)
    else:
      try:
        event['body'] = json.loads(event['body'] or '{}')
      except:
        event['body'] = {}
  debug('event=====', event)
  try:
    handler = routes[action]
  except:
    pass
  return handler(event)