"""
config module, load user config.py to extend default config
"""

import os
from os.path import dirname, realpath, join
import pydash as _
import imp
from .common import path_import, assign_module, printError

def initConfig(conf):
  try:
    dir_path = dirname(realpath(__file__))
    configPath = join(dir_path, 'config_default.py')
    defaultConfig = path_import('ringcentral_bot_framework.core.defaultConfig', configPath)
    configAll = defaultConfig
    configAll = assign_module(configAll, conf)
  except Exception as e:
    printError(e)

  return configAll