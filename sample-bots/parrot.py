"""
Sample Parrot Bot

This bot responds to any message by repeated what was said to it. 
"""
__name__ = 'localConfig'
__package__ = 'ringcentral_bot_framework'

import copy

def botJoinPrivateChatAction(bot, groupId, user, dbAction):
  """
  This is invoked when the bot is added to a private group. 
  """
  bot.sendMessage(
    groupId,
    {
      'text': f'Hello, I am a parrot. Please reply "![:Person]({bot.id})" if you want to talk to me.'
    }
  )

def botGotPostAddAction(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction,
  handledByExtension
):
  """
  This is invoked when the user sends a message to the bot.
  """
  if handledByExtension:
    return

  if f'![:Person]({bot.id})' in text:
    bot.sendMessage(
      groupId,
      {
        'text': f'![:Person]({creatorId}), you just posted "{text}".'
      }
    )

