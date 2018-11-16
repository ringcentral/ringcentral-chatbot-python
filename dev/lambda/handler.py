import json
from .core.route import router

def hello(event, context):

    return router(event)

