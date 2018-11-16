"""
common props, function
"""

import sys, os
import pydash as _
import json

isProduction = False
try:
  isProduction = os.environ['ENV'] == 'production'
except:
  isProduction = False

tables = ('bot', 'user')

def debug(*argv):
  if isProduction:
    return
  print(argv)

def result(
  msg,
  status = 200,
  options = {}
):
  return _.assign({
    'statusCode': status,
    'body': msg,
  }, options)

def subscribeInterval():
  return '/restapi/v1.0/subscription/~?threshold=59&interval=15'

def defaultEventHandler(event):
  return {
    'statusCode': 200,
    'body': json.dumps(event)
  }