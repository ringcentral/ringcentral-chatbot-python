"""
db wrapper
"""
import os
import pydash as _
import imp
from core.filedb import action

builtInDbs = ['filedb', 'dynamodb']
dbType = 'filedb'
dbAction = action
try:
  dbPath = os.environ['DB_TYPE']
  if dbPath in builtInDbs:
    dbPath = './' + dbType + '.py'
  imp.load_source('db', dbPath)
  from db import action as realAction
  dbAction = realAction
except:
  dbType = 'filedb'