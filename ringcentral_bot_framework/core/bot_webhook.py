from .common import result
from .bot import Bot, getBot
import time
from .config import configAll

botJoinPrivateChatAction = configAll.botJoinPrivateChatAction
botGotPostAddAction = configAll.botGotPostAddAction

def botWebhook(event):
  message = event.body
  body = message.body
  defaultResponse = result('bot WebHook replied', 200, {
    'headers': {
      'validation-token': event.headers['validation-token'] or event.headers['Validation-Token']
    }
  })
  if body == None:
    return defaultResponse

  botId = message.ownerId
  eventType = body.eventType
  groupId = body.id
  bot = getBot(botId)
  if not bot:
    return defaultResponse

  if eventType == 'GroupJoined':
    botJoinPrivateChatAction(bot, groupId)

  elif eventType == 'PostAdded':
    # for bot self post, ignore
    if body.creatorId == botId:
      return defaultResponse
    botGotPostAddAction(bot, groupId, body.text)

  return defaultResponse