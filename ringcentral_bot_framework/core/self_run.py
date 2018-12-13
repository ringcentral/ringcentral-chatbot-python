'''
self dispatch,
used when bot auth fails, and we need retry
'''
import os
import pydash as _
import time
from .common import result, debug
from importlib import import_module
import json

def lambdaName():
  try:
    return os.environ['AWS_LAMBDA_FUNCTION_NAME']
  except:
    return False

def renewBot (event, Bot):
  """
  for self call renewbot async
  """
  debug('self tringgering, renew bot')
  if _.predicates.is_number(event['wait']):
    time.sleep(event['wait'])

  bot = Bot()
  bot.id = event.id
  event.botId
  bot.token = event.token
  bot.writeToDb()
  bot.renewWebHooks(event)
  return result('Bot renew done')

def selfTrigger(event, Bot):
  debug('self tringgering')
  name = lambdaName()
  if not name:
    return renewBot(event, Bot)
  boto3 = import_module('boto3')
  client = boto3.client('lambda')
  client.invoke(
      FunctionName=name,
      InvocationType='Event',
      ClientContext='string',
      Payload=json.dumps(event)
  )
  time.sleep(event['wait'])