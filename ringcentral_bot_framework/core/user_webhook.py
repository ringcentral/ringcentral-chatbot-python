from .common import result, subscribeInterval
from .user import User, getUser
from .bot import Bot, getBot
import time
from .config import configAll

botJoinPrivateChatAction = configAll.botJoinPrivateChatAction
botGotPostAddAction = configAll.botGotPostAddAction
userEventAction = configAll.userEventAction
subscribeIntervalText = subscribeInterval()

def userWebhook(event):
  message = event.body
  body = message.body
  defaultResponse = result('user WebHook replied', 200, {
    'headers': {
      'validation-token': event.headers['validation-token'] or event.headers['Validation-Token']
    }
  })
  if body == None:
    return defaultResponse

  userId = body.extensionId or message.ownerId
  eventType = body.eventType
  groupId = body.id
  user = getUser(userId)
  isRenewEvent = message.event == subscribeIntervalText
  if user == False:
    return defaultResponse

  if isRenewEvent:
    user.renewWebHooks(event)
    user.refresh()
    return defaultResponse

  else:
    userEventAction(
      user,
      eventType,
      groupId,
      event,
      Bot,
      getBot
    )
