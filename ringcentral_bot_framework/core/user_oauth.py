"""
user auth
"""
import time
from .common import result
from pydash import get

def initUserAuth(
  conf,
  Bot,
  getBot,
  User,
  dbAction
):
  def userAuth(event):
    user = User()
    code = get(event, 'queryStringParameters.code[0]') or get(event, 'queryStringParameters.code')
    user.auth(code)
    state = get(event, 'queryStringParameters.state[0]') or get(event, 'queryStringParameters.state') or ','
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
  return userAuth

