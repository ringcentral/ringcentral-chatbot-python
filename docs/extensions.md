
# Using Bot Extensions

RingCentral Chatbot Framework for Python Extensions will extend bot command support.

Just add extensions in your bot config file:

```python

'''
use extensions
example:
'''
import ringcentral_bot_framework_extension_botinfo as wt
extensions = [wt]
```

## Write a extension

Write one extension will be simple, just check out [botinfo extension](https://github.com/zxdong262/ringcentral-chatbot-python-ext-bot-info) as an example, you just need to write one function there.

```python
# botinfo extension's source code
# https://github.com/zxdong262/ringcentral-chatbot-python-ext-bot-info/blob/master/ringcentral_bot_framework_extension_botinfo/__init__.py
import json

name = 'ringcentral_bot_framework_extension_botinfo'

def botGotPostAddAction(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction
):
  """
  bot got group chat message: text
  bot extension could send some response
  return True when bot send message, otherwise return False
  """
  if not f'![:Person]({bot.id})' in text:
    return False

  if 'bot info' in text:
    botInfo = bot.platform.get('/account/~/extension/~')
    txt = json.loads(botInfo.text())
    txt = json.dumps(txt, indent=2)
    msg = f'![:Person]({creatorId}) bot info json is:\n' + txt

    bot.sendMessage(
      groupId,
      {
        'text': msg
      }
    )
    return True
  else:
    return False

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
  return None

def route(event, framework):
  '''
  custom route example
  handle '/ext-custom'
  '''
  action = ''
  try:
    action = event['pathParameters']['action']
    if not action == 'ext-custom':
      return None

    listBots = framework.dbAction('bot', 'get', None)
    return {
      'statusCode': 200,
      'body': json.dumps(listBots)
    }

  except Exception as e:
    print(e)
    return None

def defaultEventHandler(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction,
  handledByExtension,
  event
):
  """
  default event handler, for event not match any above
  """
  return
```