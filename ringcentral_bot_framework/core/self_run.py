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

def selfTrigger(event, Bot):
  debug('self tringgering')
  name = lambdaName()
  if not name:
    botAuth = import_module('ringcentral_bot_framework.core.bot_oauth')
    return botAuth.renewBot(event)
  boto3 = import_module('boto3')
  client = boto3.client('lambda')
  client.invoke(
      FunctionName=name,
      InvocationType='Event',
      ClientContext='string',
      Payload=json.dumps(event)
  )
  time.sleep(2)