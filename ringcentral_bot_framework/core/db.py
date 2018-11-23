"""
db wrapper
"""
import os
from os.path import dirname, realpath, join, isabs
import pydash as _
import importlib.util
from .filedb import action, dbName
from .common import debug, path_import
from .config import configAll as conf

builtInDbs = ['filedb', 'dynamodb']
dbType = 'filedb'
dbAction = action
DBNAME = dbName

try:
  dbType = os.environ['DB_TYPE']
except:
  pass

pdbName = 'ringcentral_bot_framework.custom_db'

try:
  if dbType in builtInDbs:
    dir_path = dirname(realpath(__file__))
    dbPath = join(dir_path, dbType + '.py')
    pdbName = 'ringcentral_bot_framework.core.' + dbType
    db = path_import(pdbName, dbPath)
    dbAction = db.action
    DBNAME = db.dbName
  elif dbType == 'custom':
    DBNAME = conf.dbName()
    dbAction = conf.dbWrapper

except Exception as e:
  debug(e)

type2 = 'custom'
if dbType in builtInDbs:
  type2 = 'built-in'
print('Use database', type2, DBNAME)