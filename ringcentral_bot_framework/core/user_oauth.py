"""
user auth
"""
import time
from .common import result
from .user import User
from .bot import Bot, getBot
from .config import configAll as conf
from .db import dbAction
from pydash import get

def userAuth(event):
  user = User()
  user.auth(get(event, 'queryStringParameters.code'))
  state = get(event, 'queryStringParameters.state') or ','
  arr = state.split(',')
  groupId = get(arr, '[0]')
  botId = get(arr, '[1]')
  bot = getBot(botId)
  user.addGroup(groupId, botId)
  conf.userAuthSuccessAction(bot, groupId, user.id, dbAction)
  conf.userAddGroupInfoAction(user, bot, groupId, dbAction)
  return result(
    conf.userAuthSuccessHtml(user, bot),
    200,
    {
      'headers': {
        'Content-Type': 'text/html; charset=UTF-8'
      }
    }
  )

