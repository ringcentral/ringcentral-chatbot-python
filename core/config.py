"""
config module, load user config.py to extend default config
"""

import os
import pydash as _
import imp
import core.config as defaultConfig
from core.common import debug

config = defaultConfig
try:
  cwd = os.getcwd()
  configPath = os.path.join(cwd, 'config.py')
  imp.load_source('userConfig', configPath)
  import userConfig
  _.assign(config, userConfig)
except:
  debug('no user config.py, use default config')