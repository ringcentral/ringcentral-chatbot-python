"""
config module, load user config.py to extend default config
"""

import os
from os.path import dirname, realpath, join
import pydash as _
import imp
from .common import path_import, assign_module, printError

dir_path = dirname(realpath(__file__))
configPath = join(dir_path, 'config_default.py')
defaultConfig = path_import('ringcentral_bot_framework.core.defaultConfig', configPath)
configAll = defaultConfig

try:
  cwd = os.getcwd()
  configPath = os.path.join(cwd, 'config.py')
  if os.access(configPath, os.R_OK):
    userConfig = path_import('ringcentral_bot_framework.localConfig', configPath)
    configAll = assign_module(configAll, userConfig)
    print('use local config.py')
  else:
    print('no local config.py, use default config')
except Exception as e:
  printError(e)
