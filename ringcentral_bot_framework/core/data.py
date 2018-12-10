'''
data viewer
'''
import pydash as _
from .db import dbAction
from .config import configAll
from .common import result
import json
import os

tables = list(map(lambda x: x['name'], configAll.dbTables()))

disabled = True
try:
  disabled = os.environ['DATA_VIEWER_ENABLED'] != 'yes'
except:
  pass

def dataView(event):
  if disabled:
    return result('Data viewer diabled, set DATA_VIEWER_ENABLED=yes to enable it')
  tableName = _.get(event, 'queryStringParameters.tableName') or 'bot'
  if not tableName in tables:
    return result('tableName not right', 400)
  res = dbAction(tableName, 'get')
  return result(
    '<pre>' + json.dumps(res, indent=2) + '</pre>',
    400
  )