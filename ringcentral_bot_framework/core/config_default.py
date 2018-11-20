"""
default config module
could write config.py to override all the bot behavior
"""
__name__ = 'defaultConfig'
__package__ = 'ringcentral_bot_framework.core'

def userAuthSuccessMessage(userId):
  """
  user auth bot app to access user data success,
  bot would send this message to chat group
  """
  return {
    'text': f'![:Person]({userId}), you have successfully authorized me to access your RingCentral data!'
  }

def userAddGroupInfoActiob(bot, user):
  """
  user add group and bot connect info,
  bot or user could do something about it,
  default: do nothing
  """
  return

def userAuthSuccessHtml():
  """
  user auth success, would see this html from browser
  """
  return '<div style="text-align: center;font-size: 20px;border: 5px solid #08c;padding: 30px;">You have authorized the bot to access your RingCentral data! Please close this page and get back to Glip</div>'

def botJoinPrivateChatAction(bot, groupId):
  """
  bot join private chat event handler
  bot could send some some welcome message
  """
  bot.sendMessage(
    groupId,
    {
      'text': f'Hello, I am a chatbot.'
    }
  )

def botGotPostAddAction(bot, groupId, creatorId, text):
  """
  bot join private chat event handler
  bot could send some some welcome message
  """
  bot.sendMessage(
    groupId,
    {
      'text': f'![:Person]({creatorId}), Hello, you just post "{text}".'
    }
  )

def userEventAction(
  user,
  eventType,
  groupId,
  event,
  Bot,
  getBot
):
  """
  bot got subscribed user event,
  do something about it
  """
  return

