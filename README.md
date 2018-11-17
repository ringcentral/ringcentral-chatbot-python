
# ringcentral-chatbot-python

RingCentral Chatbot Framework for Python

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
- `pip3 install python-dotenv ringcentral pydash boto3`

## Dev

```bash

```

## Unit Test

```bash
bin/test
```