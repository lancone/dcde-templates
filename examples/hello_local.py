#!/bin/env python3
#
#  Simple local threads hello
#

import parsl
from parsl.config import Config
from parsl.configs.local_threads import config
from parsl.app.app import python_app, bash_app

parsl.clear()
parsl.load(config)

@python_app()
def hello():
        return 'Hello World'

print(parsl.__version__)
print(hello().result())