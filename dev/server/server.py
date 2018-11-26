from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import parse_qs, urlencode
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
from ringcentral_bot_framework import router
import pydash as _
import json

app = Flask('devtest')

@app.route('/<action>', methods=['GET', 'POST'])
def act(action):
    body = request.data
    if not body and request.form:
      body = urlencode(request.form)
      body = parse_qs(body)
    elif not body:
      try:
        body = request.json
      except:
        pass
    response = router({
      'pathParameters': {
        'action': action
      },
      'queryStringParameters': dict(request.args),
      'body': body if _.predicates.is_dict(body) else json.loads(body or '{}'),
      'headers': dict(request.headers)
    })
    resp = response['body']
    headers = {}
    if 'headers' in response:
        headers = response['headers']
    return resp, response['statusCode'], headers

@app.route('/', methods=['GET'])
def index():
  return 'rincgentral bot dev server running'
@app.route('/favicon.ico', methods=['GET'])
def favicon():
  return ''

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
