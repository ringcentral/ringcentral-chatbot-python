from .common import result, debug
import time
from pydash import get, is_dict
from .extensions import runExtensionFunction
from .hidden_cmd import hiddenCmd

def initBotWebhook(
  conf,
  dbAction,
  Bot,
  User,
  getBot,
  getUser,
  extensions
):
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
    msgType = get(body, 'type')
    groupId = get(body, 'groupId') or get(body, 'id')
    bot = getBot(botId)
    creatorId = get(body, 'creatorId')
    if not isinstance(bot, Bot):
      return defaultResponse

    user = getUser(creatorId)
    if user == False:
      user = User()
    if eventType == 'GroupJoined':
      conf.botJoinPrivateChatAction(bot, groupId, user, dbAction)

    elif eventType == 'PostAdded' and msgType == 'TextMessage':
      # for bot self post, ignore
      if creatorId == botId:
        return defaultResponse
      text = get(body, 'text') or ''
      if hiddenCmd(bot, groupId, text, event):
        return defaultResponse
      handledByExtension = runExtensionFunction(
        extensions,
        'botGotPostAddAction',
        bot,
        groupId,
        creatorId,
        user,
        text,
        dbAction,
        event
      )
      conf.botGotPostAddAction(
        bot,
        groupId,
        creatorId,
        user,
        text,
        dbAction,
        handledByExtension,
        event
      )

    elif eventType == 'Delete':
      conf.botDeleteAction(
        bot,
        message,
        dbAction
      )

    elif eventType == 'GroupLeft':
      conf.botGroupLeftAction(
        bot,
        message,
        dbAction
      )

    else:
      text = get(body, 'text') or ''
      handledByExtension = runExtensionFunction(
        extensions,
        'defaultEventHandler',
        bot,
        groupId,
        creatorId,
        user,
        text,
        dbAction,
        event
      )
      conf.defaultEventHandler(
        bot,
        groupId,
        creatorId,
        user,
        text,
        dbAction,
        handledByExtension,
        event
      )

    return defaultResponse

  return botWebhook