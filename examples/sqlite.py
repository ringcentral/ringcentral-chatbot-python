import sqlite3
import os
import json
import pydash as _

fileName = 'sqlite3.db'
try:
  fileName = os.environ['SQLITE_DB_NAME']
except:
  pass

conn = sqlite3.connect(fileName)
cur = conn.cursor()
tbs = []

def tableExist(tableName):
  sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';"
  res = cur.execute(sql)
  return not res.fetchone() is None

def prepareDb(tables):
  global tbs
  tbs = tables
  for table in tables:
    name = table['name']
    if tableExist(name):
      continue
    schemas = table['schemas']
    st = f'create table {name} ('
    i = 0
    prim = None
    for s in schemas:
      n = s['name']
      t = s['type']
      if prim is None and 'primary' in s and s['primary']:
        prim = n
      tp = t == 'string' or t == 'json'
      pre = '' if i == 0 else ','
      st = st + f'{pre}{n} {tp}'
      i = i + 1
    st = st + f', PRIMARY KEY ({prim}))'
    cur.execute(st)
    conn.commit()

def getOne(tableName, id):
  st = f"select * from {tableName} where id='{id}';"
  cur.execute(st)
  res = cur.fetchone()
  if not _.predicates.is_tuple(res):
    return False
  obj = {}
  dbDef = _.collections.find(tbs, lambda x: x['name'] == tableName)
  opts = dbDef['schemas']
  i = 0
  for opt in opts:
    tp = opt['type']
    nm = opt['name']
    v = res[i]
    obj[nm] = json.loads(v) if tp == 'json' else v
    i = i + 1
  return obj

def delOne(tableName, id):
  st = f"DELETE FROM {tableName} WHERE id='{id}';"
  cur.execute(st)
  conn.commit()

def updateOne(tableName, id, update):
  keys = update.keys()
  i = 0
  ss = ''
  for k in keys:
    pre = '' if i == 0 else ','
    v = json.dumps(update[k])
    ss = ss + f"{pre}{k} = '{v}'"
    i = i + 1

  st = f"update {tableName} set {ss} WHERE id='{id}';"
  cur.execute(st)
  conn.commit()

def addOne(tableName, item):
  keys = item.keys()
  i = 0
  cs = ''
  vs = ''
  defs = _.collections.find(
    tbs,
    lambda x: x['name'] == tableName
  )
  schemas = defs['schemas']
  if defs is None:
    return False
  for k in keys:
    pre = '' if i == 0 else ', '
    schema = _.collections.find(
      schemas,
      lambda x: x['name'] == k
    )
    if schema is None:
      continue
    v = json.dumps(item[k]) if schema['type'] == 'json' else item[k]
    cs = cs + f"{pre}'{k}'"
    vs = vs + f"{pre}'{v}'"
    i = i + 1

  st = f"insert into {tableName} ({cs}) values ({vs});"
  cur.execute(st)
  conn.commit()
