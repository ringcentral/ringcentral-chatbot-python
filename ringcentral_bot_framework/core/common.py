"""
common props, function
"""

import sys, os
import pydash as _
import json
from datetime import datetime
import importlib.util
from contextlib import contextmanager

isProduction = False

try:
  isProduction = os.environ['ENV'] == 'production'
except:
  pass

def assign_module(src, ext):
  for key in dir(ext):
    if not _.strings.starts_with(key, '__'):
      setattr(src, key, getattr(ext, key))
  return src

@contextmanager
def add_to_path(p):
    old_path = sys.path
    sys.path = sys.path[:]
    sys.path.insert(0, p)
    try:
        yield
    finally:
        sys.path = old_path

def path_import(name, absolute_path):
  '''implementation taken from https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly'''
  with add_to_path(os.path.dirname(absolute_path)):
    spec = importlib.util.spec_from_file_location(name, absolute_path, submodule_search_locations=[])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def now():
  return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def debug(*argv):
  if isProduction:
    return
  print(now(), argv)

def printError(e, type = ''):
  print(now(), type + ' error:')
  print(e)

def result(
  msg = '',
  status = 200,
  options = {}
):
  return _.assign({
    'statusCode': status,
    'body': msg or '',
  }, options)

def subscribeInterval():
  return '/restapi/v1.0/subscription/~?threshold=59&interval=15'

def defaultEventHandler(event):
  return {
    'statusCode': 200,
    'body': json.dumps(event)
  }