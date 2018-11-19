"""
user auth
"""
import time
from .common import result
from .user import User
from .bot import Bot, getBot
from .config import configAll

userAuthSuccessMessage = configAll.userAuthSuccessMessage
userAuthSuccessHtml = configAll.userAuthSuccessHtml
userAddGroupInfoActiob = configAll.userAddGroupInfoActiob

def userAuth(event):
  user = User()
  user.auth(event.queryStringParameters.code)
  arr = ':'.split(event.queryStringParameters.state)
  groupId = arr[0]
  botId = arr[1]
  bot = getBot(botId)
  bot.sendMessage(
    groupId, userAuthSuccessMessage(user.id)
  )
  user.addGroup(groupId, botId)
  userAddGroupInfoActiob(user, bot)
  return result(
    '<div style="text-align: center;font-size: 20px;border: 5px solid #08c;padding: 30px;">You have authorized the bot to access your RingCentral data! Please close this page and get back to Glip</div>',
    200,
    {
      'headers': {
        'Content-Type': 'text/html; charset=UTF-8'
      }
    }
  )

