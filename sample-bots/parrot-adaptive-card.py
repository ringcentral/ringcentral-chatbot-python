'''
Sample Parrot Bot

This bot responds to any message by repeated what was said to it. 
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
                    'text': 'I am a chat bot',
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
    '''
    if handledByExtension:
        return

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
                        'text': f'![:Person]({creatorId}), Hello, you just posted "{text}"'
                    }
                ]
            }
        )