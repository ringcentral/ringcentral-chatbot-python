"""
config module, load user config.py to extend default config
"""

import os
import pydash as _
import imp
import core.config_default as defaultConfig
from core.common import debug

configAll = defaultConfig
try:
  cwd = os.getcwd()
  configPath = os.path.join(cwd, 'config.py')
  if os.access(configPath, os.R_OK):
    imp.load_source('userConfig', configPath)
    import userConfig
    _.assign(configAll, userConfig)
except:
  debug('no user config.py, use default config')