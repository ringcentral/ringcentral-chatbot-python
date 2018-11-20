
# ringcentral-chatbot-python

RingCentral Chatbot Framework for Python.

For js developer, we have [ringcentral-chatbot-js](https://github.com/tylerlong/ringcentral-chatbot-js)

## Features

- Token management
- Token/subscribe auto renew
- Built-in suport for filedb and AWS dynamodb
- Stateless, built-in suport for AWS lambda
- Define custom bot behavior by `config.py`
- Support fully customized db module, loaded when runtime check DB_TYPE
- Custom every step of bot lifecycle throught `config.py`, including bot auth, bot webhook

## Prerequisites

- Python3 and Pip3
- Nodejs 8.10+/npm, use nvm to install nodejs/npm, https://github.com/creationix/nvm
- `pip3 install python-dotenv ringcentral pydash boto3 flask`
- Create the bot App: Login to [developer.ringcentral.com](https://developer.ringcentral.com) and create an `public` `Server/Bot` app with permissions: `ReadContacts, ReadMessages, ReadPresence, Contacts, ReadAccounts, SMS, InternalMessages, ReadCallLog, ReadCallRecording, WebhookSubscriptions, Glip`

## Development

```bash
git clone git@github.com:zxdong262/ringcentral-chatbot-python.git
cd ringcentral-chatbot-python

# use virtualenv
pip3 install virtualenv # might need sudo

# init virtual env
virtualenv venv --python=python3

# use env
source ./venv/bin/activate

# install deps
pip install python-dotenv ringcentral pydash boto3 flask pylint

# run ngrok proxy
# require npm, use nvm to install nodejs to get npm https://github.com/creationix/nvm
./bin/proxy
# will show:
# Forwarding https://xxxxx.ngrok.io -> localhost:8989

# create env file
cp .sample.env .env
# then edit .env, set proper setting,
# and goto your ringcentral app setting page, set OAuth Redirect URI to https://https://xxxxx.ngrok.io/bot-oauth
RINGCENTRAL_BOT_SERVER=https://xxxxx.ngrok.io

## for bots auth required, get then from your ringcentral app page
RINGCENTRAL_BOT_CLIENT_ID=
RINGCENTRAL_BOT_CLIENT_SECRET=

# create custom bot config file, edit custom functions to define bot behavior
cp config.sample.py config.py

# run local dev server
./bin/start
```

## Test bot

- Goto your ringcentral app's bot section, click 'Add to glip'
- Login to https://glip-app.devtest.ringcentral.com, find the bot by searching its name. Talk to the bot.
- Edit config.py to change bot bahavior and test in https://glip-app.devtest.ringcentral.com

## Building and Deploying to AWS Lambda

AWS Lambda with API Gateway and DynamoDB would give us a flexible way to deploy the bot.

*Be aware that AWS Lambda **ONLY works in linux** on an x64 architecture. For **non-linux os**, we need **docker** to build dependencies, should [install docker](https://docs.docker.com/docker-for-mac/) first.

Get an AWS account, create `aws_access_key_id` and `aws_secret_access_key` and place them in `~/.aws/credentials`, like this:

```bash
[default]
aws_access_key_id = <your aws_access_key_id>
aws_secret_access_key = <your aws_secret_access_key>
```

For more information, refer to https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html

```bash
cp dev/lambda/serverless.sample.yml devlambda/serverless.yml
```

Edit `lambda/serverless.yml`, and make sure you set the proper name and required env.

```yml
# you can define service wide environment variables here
  environment:
    NODE_ENV: production
    # ringcentral apps

    ## bots
    RINGCENTRAL_BOT_CLIENT_ID:
    RINGCENTRAL_BOT_CLIENT_SECRET:

    ## user
    RINGCENTRAL_USER_CLIENT_ID: xxxx
    RINGCENTRAL_USER_CLIENT_SECRET: xxxx

    ## common
    RINGCENTRAL_SERVER: https://platform.devtest.ringcentral.com
    RINGCENTRAL_BOT_SERVER: https://xxxx.execute-api.us-east-1.amazonaws.com/default/poc-your-bot-name-dev-bot

    # db
    DB_TYPE: dynamodb
    DYNAMODB_TABLE_PREFIX: rc_bot2
    DYNAMODB_REGION: us-east-1

```

Deploy to AWS Lambda with `bin/build`

```bash
# Run this cmd to deploy to AWS Lambda, full build, may take more time
bin/build

## watch Lambda server log
bin/watch

```

- Create API Gateway for your Lambda function, shape as `https://xxxx.execute-api.us-east-1.amazonaws.com/default/poc-your-bot-name-dev-bot/{action+}`
- Make sure your Lambda function role has permission to read/write dynamodb(Set this from AWS IAM roles, could simply attach `AmazonDynamoDBFullAccess` and `AWSLambdaRole` policies to Lambda function's role)
- Make sure your Lambda function's timeout more than 5 minutes
- Do not forget to set your RingCentral app's redirect URL to Lambda's API Gateway URL, `https://xxxx.execute-api.us-east-1.amazonaws.com/default/poc-your-bot-name-dev-bot/bot-oauth` for bot app.

## Unit Test

```bash
bin/test
```

## Todos
Visit https://github.com/zxdong262/ringcentral-chatbot-python/issues

## License

MIT