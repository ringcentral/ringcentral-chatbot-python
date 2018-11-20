
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

## Unit Test

```bash
bin/test
```

## Todos
Visit https://github.com/zxdong262/ringcentral-chatbot-python/issues

## License

MIT