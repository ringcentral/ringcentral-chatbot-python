
from ringcentral_bot_framework import frameworkInit
import config as conf

# import ringcentral_bot_framework_extension_botinfo as botinfo
# import ringcentral_bot_framework_extension_world_time as wt
# framework = frameworkInit(conf, [botinfo, wt])

framework = frameworkInit(conf)

def bot(event, context):

  return framework.router(event)