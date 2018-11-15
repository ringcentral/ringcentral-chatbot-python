"""
dynamodb
"""
import pydash as _
import sys, os
import boto3
import json
from core.common import tables, debug
from os.path import join
from functools import reduce

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
  prefix = 'ringcentral_bot'

def createTableName(table):
  return prefix + '_' + table

def describeTable(tableName):
  try:
    state = client.describe_table(
      TableName=tableName
    )
    return state.Table.TableStatus
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
        'AttributeName': 'is',
        'AttributeType': 'S'
      }
    ],
    ProvisionedThroughput={
      'ReadCapacityUnits': DYNAMODB_ReadCapacityUnits,
      'WriteCapacityUnits': DYNAMODB_WriteCapacityUnits
    }
  )
  for i in range(100):
    debug(i)
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

# function formatItem(item, table) {
#   return Object.keys(item)
#     .reduce((prev, key) => {
#       let type = _.get(
#         dynamodbDefinitions,
#         `${table}.${key}[1]`
#       )
#       let v = _.get(item, `${key}.S`)
#       if (!type) {
#         v = JSON.parse(v)
#       }
#       return {
#         ...prev,
#         [key]: v
#       }
#     }, {})
# }

def putItem(item, table):
  try:
    def reducer(x, y):
      v = item[y]
      if isinstance(v, dict):
        v = json.dumps(v)
      x[y] = {
        'S': v
      }
      return x
    client.putItem(
      TableName=createTableName(table),
      Item=reduce(reducer, item.keys, {})
    )
    return True
  except:
    return False

def removeItem(id, table):
  try:
    client.deleteItem(
      TableName=createTableName(table),
      Key={
        'id': {
          'S': id
        }
      }
    )
    return True
  except:
    return False

def formatItem(item):
  def reducer(x, y):
    v = item[y]
    if y != 'id':
      v = json.load(v)
    x[y] = v
    return x
  return reduce(reducer, item.keys())

def getItem(id, table):
  try:
    res = client.getItem(
      TableName=createTableName(table),
      Key={
        'id': {
          'S': id
        }
      }
    )
    return formatItem(res.Item)
  except:
    return False

def scan(table):
  try:
    res = client.getItem(
      TableName=createTableName(table)
    )
    return map(formatItem, res.Items)
  except:
    return False


def action(tableName, action, data):
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