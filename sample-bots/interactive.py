'''
Sample Bot with adaptive card and interactive message support
'''
__name__ = 'localConfig'
__package__ = 'ringcentral_bot_framework'

import copy


def botJoinPrivateChatAction(bot, groupId, user, dbAction):
    '''
    This is invoked when the bot is added to a private group.
    '''
    # bot.sendMessage(
    #     groupId,
    #     {
    #         'text': f'Hello, I am a parrot. Please reply '![:Person]({bot.id})' if you want to talk to me.'
    #     }
    # )
    '''
    use adaptive card
    check https://adaptivecards.io/ for more detail
    '''
    bot.sendAdaptiveCard(
        groupId,
        {

            '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
            'type': 'AdaptiveCard',
            'version': '1.3',
            'body': [
                {
                    'type': 'TextBlock',
                    'text': 'hello!',
                    'size': 'large'
                },
                {
                    'type': 'TextBlock',
                    'text': 'Hi, I am a chat bot',
                    'weight': 'bolder'
                }
            ]
        }
    )



def botGotPostAddAction(
    bot,
    groupId,
    creatorId,
    user,
    text,
    dbAction,
    handledByExtension,
    event
):
    '''
    This is invoked when the user sends a message to the bot.
    To use interactive messages, make sure add `groupId` and `botId` to action data
    '''
    if handledByExtension:
        return
    msg = text.replace(f'![:Person]({bot.id})', '')

    if f'![:Person]({bot.id})' in text:
        bot.sendAdaptiveCard(
            groupId,
            {
                '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
                'type': 'AdaptiveCard',
                'version': '1.3',
                'body': [
                    {
                        'type': 'TextBlock',
                        'text': 'Hello'
                    },
                    {
                        'type': 'TextBlock',
                        'text': f'You just posted "{msg}"'
                    }
                ],
                'actions': [
                  {
                    'type': 'Action.Submit',
                    'title': 'OK, Polly, you are smart',
                    'data': {
                      'groupId': groupId,
                      'botId': bot.id
                    }
                  }
                ]
            }
        )

def onInteractiveMessage(
  bot,
  groupId,
  userInfo,
  data,
  dbAction,
  handledByExtension,
  event
):
  """
  bot got interactive message from user action in ringcentral app adaptive cards,
  do something about it
  default: do nothing
  """
  print('groupId', groupId)
  print('userInfo', userInfo)
  print('data', data)
  userName = userInfo['firstName']
  bot.sendAdaptiveCard(
      groupId,
      {
          '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
          'type': 'AdaptiveCard',
          'version': '1.3',
          'body': [
              {
                  'type': 'TextBlock',
                  'text': 'Great'
              },
              {
                  'type': 'TextBlock',
                  'text': f'You are smart too, {userName}!'
              }
          ]
      }
  )