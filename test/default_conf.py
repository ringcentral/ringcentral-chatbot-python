"""
Sample Parrot Bot

This bot responds to any message by repeated what was said to it. 
"""
__name__ = 'localConfig'
__package__ = 'ringcentral_bot_framework'
def dbTables():
  """
  db tables to init
  """
  return [
    {
      'name': 'bot',
      'schemas': [
        {
          'name': 'id',
          'type': 'string',
          'primary': True
        },
        {
          'name': 'x',
          'type': 'string'
        },
        {
          'name': 'token',
          'type': 'json'
        },
        {
          'name': 'data',
          'type': 'json'
        }
      ]
    },
    {
      'name': 'user',
      'schemas': [
        {
          'name': 'id',
          'type': 'string',
          'primary': True
        },
        {
          'name': 'token',
          'type': 'json'
        },
        {
          'name': 'groups',
          'type': 'json'
        },
        {
          'name': 'data',
          'type': 'json'
        }
      ]
    }
  ]