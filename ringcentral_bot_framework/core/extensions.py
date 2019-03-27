"""
extensions load module
get extension names from env.EXTENSIONS
"""

from importlib import import_module
import os
import pydash as _


def runExtensionFunction(extensions, name, *args):
  '''
  run extension functions by name
  name must in extensionFuntionNames
  '''

  res = False
  for ext in extensions:
    func = ext.__dict__.get(name)
    hanldedByPrevious = False
    if not func is None:
      hanldedByPrevious = func(*args, res)
    res = res or hanldedByPrevious

  return res