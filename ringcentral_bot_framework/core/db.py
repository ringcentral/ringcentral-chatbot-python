"""
db wrapper
"""
import os
from os.path import dirname, realpath, join
import pydash as _
import importlib.util
from .filedb import action, dbName
from .common import debug, path_import

builtInDbs = ['filedb', 'dynamodb']
dbType = 'filedb'
dbAction = action
DBNAME = dbName

try:
  dbType = os.environ['DB_TYPE']
  dbName = os.environ['DB_MODULE_NAME']
  dbPath = os.environ['DB_MODULE_PATH']
except:
  pass

try:
  if dbType in builtInDbs:
    dir_path = dirname(realpath(__file__))
    dbPath = join(dir_path, dbType + '.py')
    pdbName = 'ringcentral_bot_framework.core.' + dbType
  db = path_import(dbName, dbPath)
  dbAction = db.action
  DBNAME = db.dbName
except Exception as e:
  debug(e)