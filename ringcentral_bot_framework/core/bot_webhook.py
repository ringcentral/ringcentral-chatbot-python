from .common import result, debug
from .bot import Bot, getBot
import time
from .config import configAll
from pydash import get, is_dict

botJoinPrivateChatAction = configAll.botJoinPrivateChatAction
botGotPostAddAction = configAll.botGotPostAddAction

def botWebhook(event):
  message = get(event, 'body')
  body = get(message, 'body')
  defaultResponse = result('bot WebHook replied', 200, {
    'headers': {
      'validation-token': get(event, 'headers.validation-token') or get(event, 'headers.Validation-Token')
    }
  })
  if not is_dict(body) :
    return defaultResponse

  botId = get(message, 'ownerId')
  eventType = get(body, 'eventType')
  groupId = get(body, 'groupId') or get(body, 'id')
  bot = getBot(botId)
  creatorId = get(body, 'creatorId')
  if not isinstance(bot, Bot):
    return defaultResponse

  if eventType == 'GroupJoined':
    botJoinPrivateChatAction(bot, groupId)

  elif eventType == 'PostAdded':
    # for bot self post, ignore
    if creatorId == botId:
      return defaultResponse
    botGotPostAddAction(bot, groupId, creatorId, body['text'])

  return defaultResponse