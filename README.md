# [ringcentral-chatbot-python](https://github.com/zxdong262/ringcentral-chatbot-python) <!-- omit in toc -->

[![Build Status](https://travis-ci.org/zxdong262/ringcentral-chatbot-python.svg?branch=test)](https://travis-ci.org/zxdong262/ringcentral-chatbot-python)

Welcome to the RingCentral Chatbot Framework for Python. This framework dramatically simplifies the process of building a bot to work with Glip, RingCentral's group chat system. It is intended to do most of the heavy lifting for developers, allowing them to focus primarily on the logic and user experience of their bot.

## Features

- **Token Management** - handles the server logic associated with bot authentication, and auth token persistence
- **Event Subscribtion** - automatically subscribes to bot events, and renews those subscriptions when they expire
- **Easy Customization** - modify bot behaviors by editing `config.py`
- **Data Persistence** - built-in suport for filedb and AWS dynamodb, with fully customizable DB layer
- **Turn-key hosting** - built-in suport for AWS lambda to host your bot

## Getting Started

Let's get a local chatbot server up and running so that you can understand how the framework functions. Our first chatbot will be a simple parrot bot that will repeat things back to you. Before we get started, let's get your development environment setup with everything you need.

### Install Prerequisites

This framework requires Python3.6+ and Pip3.

First we install [virtualenv](https://virtualenv.pypa.io/en/latest/) which will create an isolated environment in which to install and run all the python libraries needed by this framework. Using virtualenv will ensure that the libraries installed for this project do not conflict or disrupt the other python projects you are working on.

```bash
pip3 install virtualenv
virtualenv venv --python=python3
source ./venv/bin/activate
pip3 install python-dotenv ringcentral pydash boto3 flask pylint ringcentral_client
```

Next, we need to install and run [ngrok](https://ngrok.com/), a tool for routing web requests to a localhost. This is what will allow your local bot in development to receive webhooks from RingCentral. ngrok is a node app and is installed and start as follows:

```bash
npm install
./bin/proxy
```

After ngrok has started, it will display the URL when the ngrok proxy is operating. It will say something like:

```Forwarding https://xxxxx.ngrok.io -> localhost:9898```

Make note of this URL, as you will need it in the next step.

### Create Your Bot App

You will need to create your Bot App in RingCentral. Clicking the link, "Create Bot App" below will do this for you. When you click it, you will to enter in the callback URL for the bot. This will be the ngrok URL above, plus `/bot-oauth`. For example:

    https://kahsdfkhsd.ngrok.io/bot-oauth

[Create Bot App](https://developer.ringcentral.com/new-app?name=Sample+Bot+App&desc=A+sample+app+created+in+conjunction+with+the+python+bot+framework&public=false&type=ServerBot&carriers=7710,7310,3420&permissions=ReadAccounts,EditExtensions,SubscriptionWebhook,Glip&redirectUri=)

When you are finished creating your Bot Application, make note of the Client ID and Client Secret. We will use those values in the next step.

### Edit .env

A sample .env file can be found in `.env.sample`. Create a copy of this file:

```bash
cp .sample.env .env
```

Then look for the following variables, and set them accordingly:

- `RINGCENTRAL_BOT_SERVER`
- `RINGCENTRAL_BOT_CLIENT_ID`
- `RINGCENTRAL_BOT_CLIENT_SECRET`

### Install Bot Behaviors

This bot framework loads all bot behaviors from a file called `config.py`. Let's copy the parrot bot config to get started.

```bash
cp sample-bots/parrot.py ./config.py
```

### Start the Server

```bash
./bin/start
```

### Add Bot to Glip

When the server is up and running, you can add the bot to your sandbox Glip account. Navigate the dashboard for the app you created above. Select "Bot" from the left-hand sidebar menu. Save a preferred name for your bot, then click the "Add to Glip" button.

### Send a Test Message

After the bot is added, we can message with it. Login to our [sandbox Glip](https://glip.devtest.ringcentral.com). Then start a chat with the bot using the name you chose in the previous step.

You should now be in private chat session with the bot. It should greet you with a message similar to:

> Hello, I am a chatbot. Please reply "ParrotBot" if you want to talk to me.

Type `@ParrotBot Polly want a cracker?` and let's see what happens.

## Example bot apps

The following bots were created using this framework, and should serves as guides as you develop your own original bot.

- [date-time-chatbot](https://github.com/zxdong262/ringcentral-date-time-chatbot): simple Glip chatbot that can tell time/date.
- [assistant-bot](https://github.com/zxdong262/ringcentral-assistant-bot): simple assistant Glip bot to show user/company information, this bot will show you how to access user data.
- [survey-bot](https://github.com/zxdong262/ringcentral-survey-bot): example survey bot, this bot will show you how to create/use custom database wrapper.
- [translate-bot](https://github.com/zxdong262/ringcentral-translate-bot): translate bot for glip.

## Advanced Topics

### Use CLI tool to create a bot app

The [ringcentral-chatbot-factory-py](https://github.com/zxdong262/ringcentral-chatbot-factory-py) was created to help speed up the process of creating additional Glip bots. To use it, install it, then run the `rcf` command as shown below:

```bash
pip3 install ringcentral_chatbot_factory
rcf my-ringcentral-chat-bot
```

Then just answer the prompts. Then follow the directions in `my-ringcentral-chat-bot/README.md` to get up and running.

![ ](https://github.com/zxdong262/ringcentral-chatbot-factory-py/raw/master/screenshots/cli.png)

## Building and Deploying to AWS Lambda

AWS Lambda with API Gateway and DynamoDB would give us a flexible way to deploy the bot.

This requires Nodejs 8.10+/npm, and we recommend using [nvm](https://github.com/creationix/nvm) to install nodejs/npm.

*Be aware that AWS Lambda **ONLY works in linux** on an x64 architecture. For **non-linux os**, we need **docker** to build dependencies -- thus you should [install docker](https://docs.docker.com/docker-for-mac/) first.

Get an AWS account, create `aws_access_key_id` and `aws_secret_access_key` and place them in `~/.aws/credentials`, like this:

```bash
[default]
aws_access_key_id = <your aws_access_key_id>
aws_secret_access_key = <your aws_secret_access_key>
```

For more information, refer to [https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html](https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html).

Start by installing serverless and copying a sample config file for it.

```bash
npm i
cp dev/lambda/serverless.sample.yml dev/lambda/serverless.yml
```

Edit `dev/lambda/serverless.yml`, and make sure you set the proper name and required env.

```yml
  environment:
    ENV: production
    # ringcentral apps

    ## for bots auth, required
    RINGCENTRAL_BOT_CLIENT_ID:
    RINGCENTRAL_BOT_CLIENT_SECRET:

    ## for user auth, could be empty if do not need user auth
    RINGCENTRAL_USER_CLIENT_ID:
    RINGCENTRAL_USER_CLIENT_SECRET:

    ## common
    RINGCENTRAL_SERVER: https://platform.devtest.ringcentral.com
    RINGCENTRAL_BOT_SERVER: https://xxxxx.execute-api.us-east-1.amazonaws.com/dev

    # db
    DB_TYPE: dynamodb
    DYNAMODB_TABLE_PREFIX: ringcentral-bot
    DYNAMODB_REGION: us-east-1
    DYNAMODB_ReadCapacityUnits: 1
    DYNAMODB_WriteCapacityUnits: 1
```

Deploy to AWS Lambda with `bin/deploy` and should observe the following:

```bash
./bin/deploy
Service Information
service: ringcentral-bot
stage: dev
region: us-east-1
stack: ringcentral-bot-dev
api keys:
  None
endpoints:
  ANY - https://dddddd.execute-api.us-east-1.amazonaws.com/dev/{action+}
  GET - https://dddddd.execute-api.us-east-1.amazonaws.com/dev/
```

Relpace `RINGCENTRAL_BOT_SERVER: https://xxxxx.execute-api.us-east-1.amazonaws.com/dev` in serverless.yml with `RINGCENTRAL_BOT_SERVER: https://dddddd.execute-api.us-east-1.amazonaws.com/dev` and run `./bin/deploy` to deploy again.

You may watch the Lambda server log by running:

```bash
bin/watch
```

Do not forget to set your RingCentral app's redirect URL to Lambda's API Gateway URL, `https://dddddd.execute-api.us-east-1.amazonaws.com/dev/bot-oauth` for bot app.

## Using Bot Extensions

RingCentral Chatbot Framework for Python Extensions will extend bot command support with simple setting in `.env`.

Just set like this in `.env`, support multiple extensions seperated by `,`

```bash
EXTENSIONS=ringcentral_bot_framework_extension_botinfo,ringcentral_bot_framework_extension_world_time
```

And install these extensions by `pip install ringcentral_bot_framework_extension_botinfo ringcentral_bot_framework_extension_world_time`, it is done.

![ ](https://github.com/zxdong262/ringcentral-chatbot-python-ext-bot-info/raw/master/screenshots/ss.png)

You can search for more extension in [pypi.org](https://pypi.org) with keyword `ringcentral_bot_framework_extension`.

## Write a extension your self

Write one extension will be simple, just check out [botinfo extension](https://github.com/zxdong262/ringcentral-chatbot-python-ext-bot-info) as an example, you just need to write one function there.

```python
# botinfo extension's source code
# https://github.com/zxdong262/ringcentral-chatbot-python-ext-bot-info/blob/master/ringcentral_bot_framework_extension_botinfo/__init__.py
import json

name = 'ringcentral_bot_framework_extension_botinfo'

def botGotPostAddAction(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction
):
  """
  bot got group chat message: text
  bot extension could send some response
  return True when bot send message, otherwise return False
  """
  if not f'![:Person]({bot.id})' in text:
    return False

  if 'bot info' in text:
    botInfo = bot.platform.get('/account/~/extension/~')
    txt = json.loads(botInfo.text())
    txt = json.dumps(txt, indent=2)
    msg = f'![:Person]({creatorId}) bot info json is:\n' + txt

    bot.sendMessage(
      groupId,
      {
        'text': msg
      }
    )
    return True
  else:
    return False
```

## Unit Test

```bash
bin/test
```

## Todos

Visit [https://github.com/zxdong262/ringcentral-chatbot-python/issues](https://github.com/zxdong262/ringcentral-chatbot-python/issues)

## Credits

The core bot framework logic is implanted from [ringcentral-ai-bot](https://github.com/ringcentral-tutorials/ringcentral-ai-bot) written by [@tylerlong](https://github.com/tylerlong)

## License

MIT
