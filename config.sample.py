"""
sample config module
run "cp config.sample.py config.py" to create local config
edit config.py functions to override default bot behavior
"""
__name__ = 'localConfig'
__package__ = 'ringcentral_bot_framework'

def userAuthSuccessMessage(userId):
  """
  user auth bot app to access user data success,
  bot would send this message to chat group
  """
  return {
    'text': f'![:Person]({userId}), you have successfully authorized me to access your RingCentral data!'
  }

def userAddGroupInfoAction(bot, user):
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
  bot could send some welcome message or help, or something else
  """
  bot.sendMessage(
    groupId,
    {
      'text': f'Hello, I am a chatbot. Please reply "![:Person]({bot.id})" if you want to talk to me.'
    }
  )

def botGotPostAddAction(bot, groupId, creatorId, text):
  """
  bot got group chat message: text
  bot could send some response
  """
  bot.sendMessage(
    groupId,
    {
      'text': f'![:Person]({creatorId}), Hello, you just posted "{text}"'
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

