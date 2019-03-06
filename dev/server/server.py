from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
from ringcentral_bot_framework import frameworkInit
import config as conf
# import ringcentral_bot_framework_extension_botinfo as botinfo
# import ringcentral_bot_framework_extension_world_time as wt
# framework = frameworkInit(conf, [botinfo, wt])

framework = frameworkInit(conf)

app = Flask('devtest')

@app.route('/test', methods=['GET'])
def index():
  return 'RingCentral bot dev server running'
@app.route('/favicon.ico', methods=['GET'])
def favicon():
  return ''

@app.route('/<action>', methods=['GET', 'POST'])
def act(action):
  event = framework.flaskRequestParser(request, action)
  response = framework.router(event)
  resp = response['body']
  headers = {}
  if 'headers' in response:
      headers = response['headers']
  return resp, response['statusCode'], headers

port = 9898
host = 'localhost'
try:
  port = os.environ['PORT']
  host = os.environ['HOST']
except:
  pass
app.run(
  host=host,
  port=port,
  debug=True,
  load_dotenv=True
)
