"""
extensions load module
get extension names from env.EXTENSIONS
"""

from importlib import import_module
import os
import pydash as _

extensionFuntionNames = ['botGotPostAddAction']
extensionFuntion = {}

for name in extensionFuntionNames:
  extensionFuntion[name] = []

try:
  exts = os.environ['EXTENSIONS']
  print('extensions:', exts)
  arr = exts.split(',')
  for extName in arr:
    mod = import_module(extName)
    for funcName in extensionFuntionNames:
      if funcName in mod.__dict__:
        extensionFuntion[name].append(
          mod.__dict__.get(funcName)
        )
except Exception as e:
  print(e)
  pass

def runExtensionFunction(name, *args):
  '''
  run extension functions by name
  name must in extensionFuntionNames
  '''
  if not name in extensionFuntionNames:
    return

  funcs = extensionFuntion[name]
  res = False
  for func in funcs:
    hanldedByPrevious = func(*args, res)
    res = res or hanldedByPrevious

  return res