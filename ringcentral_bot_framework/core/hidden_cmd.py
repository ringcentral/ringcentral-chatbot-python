'''
support hidden command `__rename__` and `__setAvatar__`
'''

import re
import pydash as _
import requests

def hiddenCmd(
  bot,
  groupId,
  text,
  event
):
  if not f'![:Person]({bot.id})' in text:
    return False

  m2 = re.match(r'[^ ]+ +__rename__ +(.+)', text)
  m3 = re.match(r'[^ ]+ +__setAvatar__', text)
  if m2 is None and m3 is None:
    return False
  elif not m2 is None:
    name = m2.group(1)
    name = name[0:31].strip()
    bot.rename(name)
    bot.sendMessage(
      groupId,
      {
        'text': f'Renamed to {name}'
      }
    )
  else:
    attachment = _.get(event, 'body.body.attachments[0]')
    if attachment is None:
      return False
    r = requests.get(attachment['contentUri'])
    bot.setAvatar(r.content, attachment['name'])
    bot.sendMessage(
      groupId,
      {
        'text': 'Set avatar done'
      }
    )

  return True