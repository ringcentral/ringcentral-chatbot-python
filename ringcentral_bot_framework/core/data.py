'''
data viewer
'''
import pydash as _
from .common import result, getQueryParam
import json
import os

disabled = True
try:
  disabled = os.environ['DATA_VIEWER_ENABLED'] != 'yes'
except:
  pass

def initDataView(configAll, dbAction):
  def dataView(event):
    tables = list(map(lambda x: x['name'], configAll.dbTables()))
    if disabled:
      return result('Data viewer diabled, set DATA_VIEWER_ENABLED=yes to enable it')
    tableName = getQueryParam(event, 'tableName') or 'bot'
    if not tableName in tables:
      return result('tableName not right', 400)
    res = dbAction(tableName, 'get')
    return result(
      '<pre>' + json.dumps(res, indent=2) + '</pre>',
      400
    )
  return dataView