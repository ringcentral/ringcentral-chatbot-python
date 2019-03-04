from .common import result, subscribeInterval
import time
from pydash import get, is_dict

subscribeIntervalText = subscribeInterval()

def initUserWebhook(
  conf,
  Bot, getBot,
  User, getUser,
  dbAction
):
  def userWebhook(event):
    message = get(event, 'body')
    body = get(message, 'body')
    defaultResponse = result('user WebHook replied', 200, {
      'headers': {
        'validation-token': get(event, 'headers.validation-token') or get(event, 'headers.Validation-Token')
      }
    })

    if not is_dict(body):
      print('body not dict')
      return defaultResponse

    userId = get(body, 'extensionId') or get(message, 'ownerId')
    eventType = get(message, 'event')
    user = getUser(userId)
    isRenewEvent = eventType == subscribeIntervalText

    if not isinstance(user, User):
      return defaultResponse

    if isRenewEvent:
      user.renewWebHooks(event)
      user.refresh()
      return defaultResponse

    else:
      conf.userEventAction(
        user,
        eventType,
        event,
        getBot,
        dbAction
      )
      return defaultResponse
  return userWebhook