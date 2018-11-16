from flask import Flask, request, jsonify
import urllib
from core.route import router

@app.route('/<action>', methods=['GET', 'POST'])
def aws_lambda_handler(action):
    body = request.data
    if not body and request.form:
      body = urlencode(request.form)
    if not body:
      try:
        body = request.json
      except Exception as e: # not valid json
        pass
    response = router({
      'pathParameters': {
        'action': action
      },
      'queryStringParameters': request.args,
      'body': body,
      'headers': request.headers
    })

    resp = jsonify(response['body'])
    if 'headers' in response:
        resp.headers = response['headers']
    return resp, response['statusCode']

if __name__ == '__main__':
  app = Flask('devtest')
  app.run()
