'''
data viewer
'''
import pydash as _
from .db import dbAction
from .config import configAll
from .common import result
import json

tables = list(map(lambda x: x['name'], configAll.dbTables()))

def dataView(event):
  tableName = _.get(event, 'queryStringParameters.tableName') or 'bot'
  if not tableName in tables:
    return result('tableName not right', 400)
  res = dbAction(tableName, 'get')
  return result(
    '<pre>' + json.dumps(res, indent=2) + '</pre>',
    400
  )