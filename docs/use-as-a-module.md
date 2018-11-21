
# Use as a module

## Install

```bash
# install
pip3 install ringcentral_bot_framework

# create .env
wget https://raw.githubusercontent.com/zxdong262/ringcentral-chatbot-python/master/.sample.env -O .env

# create config.py
wget https://raw.githubusercontent.com/zxdong262/ringcentral-chatbot-python/master/config.sample.py -O config.py
```

## Use in flask app

```python
from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import parse_qs, urlencode
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
from ringcentral_bot_framework import router
import json

app = Flask('devtest')

@app.route('/<action>', methods=['GET', 'POST'])
def act(action):
    body = request.data
    if not body and request.form:
      body = urlencode(request.form)
    if not body:
      try:
        body = request.json
      except:
        pass
    response = router({
      'pathParameters': {
        'action': action
      },
      'queryStringParameters': dict(request.args),
      'body': json.loads(body or '{}'),
      'headers': dict(request.headers)
    })

    resp = jsonify(response['body'])
    if 'headers' in response:
        resp.headers = response['headers']
    return resp, response['statusCode']

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

```

## Use in lambda

```python
from ringcentral_bot_framework import router

def bot(event, context):

    return router(event)
```