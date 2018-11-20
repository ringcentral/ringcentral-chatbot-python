"""
dynamodb
"""
__name__ = 'dynamodb'
__package__ = 'ringcentral_bot_framework.core'

import pydash as _
import sys, os
import boto3
import json
from .common import tables, debug
from os.path import join
from functools import reduce
from pydash.predicates import is_string
from pydash.strings import starts_with

boto3.setup_default_session(region_name=os.environ['AWS_REGION'])
client = boto3.client('dynamodb')
prefix = ''
DYNAMODB_ReadCapacityUnits=5
DYNAMODB_WriteCapacityUnits=5
try:
  prefix = os.environ['DYNAMODB_TABLE_PREFIX']
  DYNAMODB_ReadCapacityUnits = os.environ['DYNAMODB_ReadCapacityUnits']
  DYNAMODB_WriteCapacityUnits = os.environ['DYNAMODB_WriteCapacityUnits']
except:
  prefix = 'ringcentral_bot_py'

dbName = 'dynamodb'

def createTableName(table):
  return prefix + '_' + table

def describeTable(tableName):
  try:
    state = client.describe_table(
      TableName=tableName
    )
    return state['Table']['TableStatus']
  except:
    return False

def createTable(table):
  name = createTableName(table)
  table = client.create_table(
    TableName=name,
    KeySchema=[
      {
        'AttributeName': 'id',
        'KeyType': 'HASH'
      }
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'id',
        'AttributeType': 'S'
      }
    ],
    ProvisionedThroughput={
      'ReadCapacityUnits': DYNAMODB_ReadCapacityUnits,
      'WriteCapacityUnits': DYNAMODB_WriteCapacityUnits
    }
  )
  for i in range(100):
    status = describeTable(name)
    if status == 'ACTIVE':
      return True
  return False

def prepareDb():
  exist = describeTable(
    createTableName(tables[0])
  )
  if exist != False:
    return True
  for t in tables:
    createTable(t)

def putItem(item, table):
  try:
    def reducer(x, y):
      v = item[y]
      if not is_string(v):
        v = json.dumps(v)
      x[y] = {
        'S': v
      }
      return x
    client.put_item(
      TableName=createTableName(table),
      Item=reduce(reducer, item.keys(), {})
    )
    return True
  except Exception as e:
    debug('dynamodb putitem error')
    debug(e)
    return False

def removeItem(id, table):
  try:
    client.delete_item(
      TableName=createTableName(table),
      Key={
        'id': {
          'S': id
        }
      }
    )
    return True
  except Exception as e:
    debug('dynamodb removeItem error')
    debug(e)
    return False

def formatItem(item):
  def reducer(x, y):
    v = item[y]['S']
    isJson = False
    try:
      isJson = v != json.loads(v)
    except:
      pass
    if isJson:
      v = json.loads(v)
    x[y] = v
    return x
  return reduce(reducer, item.keys(), {})

def getItem(id, table):
  try:
    res = client.get_item(
      TableName=createTableName(table),
      Key={
        'id': {
          'S': id
        }
      }
    )
    return formatItem(res['Item'])
  except Exception as e:
    debug('dynamodb getItem error')
    debug(e)
    return False

def scan(table):
  try:
    res = client.scan(
      TableName=createTableName(table)
    )
    return list(map(formatItem, res['Items']))
  except Exception as e:
    debug('dynamodb scan error')
    debug(e)
    return False


def action(tableName, action, data = {'id': False}):
  """db action wrapper
  * @param {String} tableName, user or bot
  * @param {String} action, add, remove, update, get
  * @param {Object} data
  * for add, {id: xxx, token: {...}, groups: {...}}
  * for remove, {id: xxx} or {ids: [...]}
  * for update, {id: xxx, update: {...}}
  * for get, singleUser:{id: xxx}, allUser: {}
  """
  debug('db op:', tableName, action, data)
  prepareDb()
  id = data['id']

  if action == 'add':
    putItem(data, tableName)

  elif action == 'remove':
    removeItem(id, tableName)

  elif action == 'update':
    update = data['update']
    old = getItem(id, tableName)
    _.assign(old, update)
    putItem(old, tableName)

  elif action == 'get':
    if id:
      return getItem(id, tableName)
    else:
      return scan(tableName)

  return action