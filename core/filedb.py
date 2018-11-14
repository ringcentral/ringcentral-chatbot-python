"""
file db
"""
import sys, os
import json
from core.common import tables, debug
from os.path import join

cwd = os.getcwd()
dbPath = join(cwd, 'filedb')

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
  toOpen = join(dbPath, tableName, id + '.json')
  if action == 'add':
    id = data['id']
    toOpen = join(dbPath, tableName, id + '.json')
    debug('to open:', toOpen)
    r = json.dumps(data, indent=2)
    with open(toOpen, 'w') as toOpenFile:
      toOpenFile.write(r)
  elif action == 'remove':
    os.remove(toOpen)
  elif action == 'get':
    with open(toOpen, 'r') as toOpenFile:
      f = toOpenFile.read()
      f = json.loads(f)
  return action
