# [RingCentral chatbot framework for Python](https://github.com/ringcentral/ringcentral-chatbot-python) <!-- omit in toc -->

[![Build Status](https://travis-ci.org/ringcentral/ringcentral-chatbot-python.svg?branch=test)](https://travis-ci.org/ringcentral/ringcentral-chatbot-python)

Welcome to the RingCentral Chatbot Framework for Python. This framework dramatically simplifies the process of building a bot to work with Glip, RingCentral's group chat system. It is intended to do most of the heavy lifting for developers, allowing them to focus primarily on the logic and user experience of their bot.

## Features

- **Token Management** - handles the server logic associated with bot authentication, and auth token persistence
- **Event Subscribtion** - automatically subscribes to bot events, and renews those subscriptions when they expire
- **Easy Customization** - modify bot behaviors by editing `bot.py`
- **Data Persistence** - built-in suport for filedb and AWS dynamodb, with fully customizable DB layer
- **Turn-key hosting** - built-in suport for AWS lambda to host your bot

## Getting Started

Let's get a local chatbot server up and running so that you can understand how the framework functions. Our first chatbot will be a simple parrot bot that will repeat things back to you. Before we get started, let's get your development environment setup with everything you need.

### Install Prerequisites

This framework requires Python3.6+ and Pip3.

First we install [virtualenv](https://virtualenv.pypa.io/en/latest/) which will create an isolated environment in which to install and run all the python libraries needed by this framework. Using virtualenv will ensure that the libraries installed for this project do not conflict or disrupt the other python projects you are working on.

```bash
# init project
bin/init
source venv/bin/activate
```

Next, we need to run [ngrok](https://ngrok.com/), a tool for routing web requests to a localhost. This is what will allow your local bot in development to receive webhooks from RingCentral. ngrok is a node app and is installed and start as follows:

```bash
./bin/proxy
```

After ngrok has started, it will display the URL when the ngrok proxy is operating. It will say something like:

```Forwarding https://xxxxx.ngrok.io -> localhost:9898```

Make note of this URL, as you will need it in the next step.

### Create Your Bot App

You will need to create your Bot App in RingCentral. Clicking the link, "Create Bot App" below will do this for you. Remember to select `messagging bot` bot and for `All RingCentral customers`, When you click it, you will to enter in the `OAuth Redirect URI ` for the bot. This will be the ngrok URL above, plus `/bot-oauth`. For example:

    https://xxxxxx.ngrok.io/bot-oauth

[Create Bot App](https://developer.ringcentral.com/new-app?name=Sample+Bot+App&desc=A+sample+app+created+in+conjunction+with+the+python+bot+framework&public=true&type=ServerBot&carriers=7710,7310,3420&permissions=ReadAccounts,EditExtensions,SubscriptionWebhook,Glip&redirectUri=)

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
cp sample-bots/parrot.py ./bot.py
```

### Start the Server

```bash
# rcs is cli server module from ringcentral_chatbot_server
rcs bot.py
```

### Add Bot to Glip

When the server is up and running, you can add the bot to your sandbox Glip account. Navigate the dashboard for the app you created above. Select "Bot" from the left-hand sidebar menu. Save a preferred name for your bot, then click the "Add to Glip" button.

### Send a Test Message

After the bot is added, we can message with it. Login to our [sandbox Glip](https://glip.devtest.ringcentral.com). Then start a chat with the bot using the name you chose in the previous step.

You should now be in private chat session with the bot. It should greet you with a message similar to:

> Hello, I am a chatbot. Please reply "ParrotBot" if you want to talk to me.

Type `@ParrotBot Polly want a cracker?` and let's see what happens.

## Quick start: Init a bot project with one line script

Now you know how it works, you may try to init a bot project in one line script:

```bash
# make sure you have python3.6+ and pip3 installed

# use wget
wget -qO- https://raw.githubusercontent.com/ringcentral/ringcentral-chatbot-factory-py/master/bin/init.sh | bash

# or with curl
curl -o- https://raw.githubusercontent.com/ringcentral/ringcentral-chatbot-factory-py/master/bin/init.sh | bash
```

A video to show the process: [https://youtu.be/x5sTrj5xSN8](https://youtu.be/x5sTrj5xSN8)

## Example bot apps

The following bots were created using this framework, and should serves as guides as you develop your own original bot.

- [date-time-chatbot](https://github.com/zxdong262/ringcentral-date-time-chatbot): simple Glip chatbot that can tell time/date.
- [assistant-bot](https://github.com/zxdong262/ringcentral-assistant-bot): simple assistant Glip bot to show user/company information, this bot will show you how to access user data.
- [poll-bot](https://github.com/zxdong262/ringcentral-poll-bot): Glip poll bot, this bot will show you how to create/use custom database wrapper.
- [translate-bot](https://github.com/zxdong262/ringcentral-translate-bot): translate bot for glip.
- [welcome-bot](https://github.com/zxdong262/ringcentral-welcome-bot-py): Glip chatbot to welcome new team member.
- [at-all-bot](https://github.com/zxdong262/ringcentral-at-all-bot): Add AT all function to glip with this bot.

## Advanced Topics

### Adaptive cards support

Check [sample-bots/parrot-adaptive-card.py](sample-bots/parrot-adaptive-card.py) as an example,
- Use `bot.sendAdaptiveCard` to send AdaptiveCard
- Use `bot.updateAdaptiveCard` to update AdaptiveCard

### Interactive message

Since we support `adaptive cards`, we also support interactive messages when using adaptive cards actions, so bot can get interactive messages directly from user actions, you need goto app setting page in `developer.ringcentral.com`, enable `Interactive Messages`, and set `https://xxxxx.ngrok.io/interactive` as `Outbound Webhook URL`

Check [sample-bots/interactive.py](sample-bots/interactive.py) as an example, define your own `onInteractiveMessage` function to handle interative messages.

### Hidden commands

- Post message `@Bot __rename__ newName` to rename bot to `newName`
- Post message `@Bot __setAvatar__` and image attachment to set bot profile image.

### Use CLI tool to create a bot app

The [ringcentral-chatbot-factory-py](https://github.com/ringcentral/ringcentral-chatbot-factory-py) was created to help speed up the process of creating additional Glip bots. To use it, install it, then run the `rcf` command as shown below:

```bash
pip3 install ringcentral_chatbot_factory
rcf my-ringcentral-chat-bot
```

Then just answer the prompts. Then follow the directions in `my-ringcentral-chat-bot/README.md` to get up and running.

![ ](https://github.com/ringcentral/ringcentral-chatbot-factory-py/raw/master/screenshots/cli.png)

- [Deploy to AWS Lambda](docs/deploy-to-aws-lambda.md)
- [Use or write extensions](docs/extensions.md)
- [Direct Use](docs/use.md)

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
