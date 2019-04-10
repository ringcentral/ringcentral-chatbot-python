# Use

## Use in Local development with Flask

```python
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
from ringcentral_bot_framework import frameworkInit

# put all bot logic in `config.py`, check `sample-bots/kitchen-sync.py` to see all the config functions
import config as conf

# Uncomments line17-19 to use extensions
# import ringcentral_bot_framework_extension_botinfo as botinfo
# import ringcentral_bot_framework_extension_world_time as wt
# framework = frameworkInit(conf, [botinfo, wt])

framework = frameworkInit(conf)

app = Flask('devtest')

@app.route('/<action>', methods=['GET', 'POST'])
def act(action):
  event = framework.flaskRequestParser(request, action)
  response = framework.router(event)
  resp = response['body']
  headers = {}
  if 'headers' in response:
      headers = response['headers']
  return resp, response['statusCode'], headers

port = 9898
host = 'localhost'

app.run(
  host=host,
  port=port,
  debug=True,
  load_dotenv=True
)

```

## Use in AWS Lambda

```python
from ringcentral_bot_framework import frameworkInit
import config as conf

# Uncomments line54-56 to use extensions
# import ringcentral_bot_framework_extension_botinfo as botinfo
# import ringcentral_bot_framework_extension_world_time as wt
# framework = frameworkInit(conf, [botinfo, wt])

framework = frameworkInit(conf)

def bot(event, context):

    return framework.router(event)

```

## Framework member functions and properties

Read [source code](../ringcentral_bot_framework/core/__init__.py) for more detail.

```py
  class BotFrameWork:
    @staticmethod
    def Bot():
      return BotClass

    @staticmethod
    def User():
      return UserClass

    @staticmethod
    def dbAction(tableName, action, data = None):
      """db action
      * make sure it it stateless,
      * in every action, you should check database is ready or not, if not, init it first
      * check https://github.com/zxdong262/ringcentral-chatbot-python/blob/master/ringcentral_bot_framework/core/dynamodb.py or https://github.com/zxdong262/ringcentral-chatbot-python/blob/master/ringcentral_bot_framework/core/filedb.py as example
      * @param {String} tableName, user or bot, or other table you defined
      * @param {String} action, add, remove, update, get
      * @param {Object} data
      * for add, {'id': 'xxx', 'token': {...}, 'groups': {...}, 'data': {...}}
      * for remove, {'id': xxx} or {'ids': [...]}
      * for update, {'id': xxx, 'update': {...}}
      * for get, singleUser:{'id': xxx}, allUser: None, query: { 'key': 'xx', 'value': 'yy' }
      """
      return dbAction(tableName, action, data = None)

    @staticmethod
    def getBot(id):
      '''
      get bot data from database, init and return bot instance, if fails or not found will return False
      '''
      return getBot(id)

    @staticmethod
    def removeBot(id):
      '''
      remove bot data from database
      '''
      return removeBot(id)

    @staticmethod
    def getUser(id):
      '''
      get user data from database, init and return user instance, if fails or not found will return False
      '''
      return getUser(id)

    @staticmethod
    def removeUser(id):
      '''
      remove user data from database
      '''
      return removeUser(id)

    @staticmethod
    def botAuth(event):
      return botAuth(event)

    @staticmethod
    def renewBot(event):
      return renewBot(event)

    @staticmethod
    def botWebhook(event):
      return botWebhook(event)

    @staticmethod
    def dataView(event):
      return dataView(event)

    @staticmethod
    def userAuth(event):
      return userAuth(event)

    @staticmethod
    def userWebhook(event):
      return userWebhook(event)

    @staticmethod
    def router(event):
      '''
      process event and return result object:
      {
        'headers': dict,
        'body': dict,
        'statusCode': number
      }
      '''
      return router(event)

    @staticmethod
    def flaskRequestParser(request, action):
      '''
      parse flask request to event format:
      {
        'pathParameters': {
          'action': string
        },
        'queryStringParameters': dict,
        'body': dict,
        'headers': dict
      }
      '''
      return flaskRequestParser(request, action)
```