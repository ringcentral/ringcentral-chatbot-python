"""
route /{action} to different event handeler
/bot-oauth bot auth
/user-oauth user auth
/bot-webhook bot webhook
/user-webhook user webhook

extend or overide default route by set `routes` in config.py
"""

from core.bot_oauth import botAuth
from core.user_oauth import userAuth
from core.bot_webhook import botWebhook
from core.user_webhook import userWebhook
from core.common import debug, defaultEventHandler

routes = {
  '/bot-oauth': botAuth,
  '/user-oauth': userAuth,
  '/bot-webhook': botWebhook,
  '/user-webhook': userWebhook
}

def router(event):
  debug('got event', event)
  action = event.pathParameters.action
  handler = routes[action] or defaultEventHandler
  return handler(event)