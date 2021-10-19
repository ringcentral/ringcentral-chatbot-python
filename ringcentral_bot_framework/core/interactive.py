"""
handle interactive message from adaptive card
"""
import time
from .common import result, getQueryParam, debug
from pydash import get
from .extensions import runExtensionFunction

def initInteractive(
  conf,
  getBot,
  dbAction,
  extensions
):
  def onInteractive(event):
    body = get(event, 'body')
    userInfo = get(body, 'user')
    data = get(body, 'data')
    botId = get(data, 'botId')
    groupId = get(data, 'groupId')
    bot = getBot(botId)
    handledByExtension = runExtensionFunction(
        extensions,
        'onInteractiveMessage',
        bot,
        groupId,
        userInfo,
        data,
        dbAction,
        event
      )
    conf.onInteractiveMessage(
      bot,
      groupId,
      userInfo,
      data,
      dbAction,
      handledByExtension,
      event
    )
    return result(
      'ok',
      200,
      {
        'headers': {
          'Content-Type': 'text/html; charset=UTF-8'
        }
      }
    )
  return onInteractive

