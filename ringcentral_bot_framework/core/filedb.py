"""
file db
"""
__name__ = 'filedb'
__package__ = 'ringcentral_bot_framework.core'

import pydash as _
import sys, os
import json
from .common import tables, debug
from os.path import join

cwd = os.getcwd()
dbPath = join(cwd, 'filedb')

dbName = 'filedb'

def assess(path):
  """
  check path exist or not
  """
  return os.access(path, os.R_OK)

def prepareDb():
  """
  prepare folders before operate
  """
  if assess(dbPath):
    return
  os.mkdir(dbPath)
  for table in tables:
    os.mkdir(
      join(dbPath, table)
    )

def readFile(toOpen):
  """
  read file as json dict
  """
  with open(toOpen, 'r') as toOpenFile:
    f = toOpenFile.read()
    f = json.loads(f)
    toOpenFile.close()
    return f

def action(tableName, action, data=None):
  """db action wrapper
  * @param {String} tableName, user or bot
  * @param {String} action, add, remove, update, get
  * @param {Object} data
  * for add, {id: xxx, token: {...}, groups: {...}}
  * for remove, {id: xxx} or {ids: [...]}
  * for update, {id: xxx, update: {...}}
  * for get, singleUser:{id: xxx}, allUser: {}
  """
  #debug('db op:', tableName, action, data)
  prepareDb()
  id = _.get(data, 'id')
  if _.predicates.is_number(id):
    id = str(id)
  if _.predicates.is_string(id):
    toOpen = join(dbPath, tableName, (id or '') + '.json')

  if action == 'add':
    id = data['id']
    toOpen = join(dbPath, tableName, id + '.json')
    r = json.dumps(data, indent=2)
    with open(toOpen, 'w+') as toOpenFile:
      toOpenFile.write(r)
      toOpenFile.close()

  elif action == 'remove':
    os.remove(toOpen)

  elif action == 'update':
    update = data['update']
    with open(toOpen, 'r+') as toOpenFile:
      f = toOpenFile.read()
      f = json.loads(f)
      _.assign(f, update)
      f = json.dumps(f, indent=2)
      toOpenFile.seek(0)
      toOpenFile.write(f)
      toOpenFile.truncate()
      toOpenFile.close()

  elif action == 'get':
    if id:
      return readFile(toOpen)
    else:
      p = join(dbPath, tableName)
      files = [f for f in os.listdir(p)]
      return list(map(lambda x: readFile(join(p, x)), files))

  return action
