"""
default config module
"""

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



