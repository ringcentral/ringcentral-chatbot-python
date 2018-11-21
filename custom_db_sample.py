"""
custom database wrapper sample file
DO NOT CHANGE __name__ and __package__
you can set dbName, eg: 'mysql'
"""
__name__ = 'custom_db'
__package__ = 'ringcentral_bot_framework'

dbName = 'xxxxxxx'

def action(tableName, action, data = {'id': False}):
  """db action wrapper
  * make sure it it stateless,
  * in every action, you should check database is ready or not, if not, init it first
  * check ringcentral_bot_framework/core/dynamodb.py or ringcentral_bot_framework/core/filedb.py for example
  * @param {String} tableName, user or bot
  * @param {String} action, add, remove, update, get
  * @param {Object} data
  * for add, {id: xxx, token: {...}, groups: {...}}
  * for remove, {id: xxx} or {ids: [...]}
  * for update, {id: xxx, update: {...}}
  * for get, singleUser:{id: xxx}, allUser: {}
  """

  # todo prepare database
  # prepareDB()

  id = data['id']

  if action == 'add':
    # todo
    pass

  elif action == 'remove':
    pass
    # todo

  elif action == 'update':
    pass
    # todo

  elif action == 'get':
    pass
    # todo

  return action