#!/bin/env python3
#
# Simple local submission to htcondor cluster.
# 
import parsl
from parsl.channels import LocalChannel
from parsl.providers import CondorProvider
from parsl.config import Config
from parsl.executors.ipp import IPyParallelExecutor
from parsl.app.app import python_app, bash_app

config = Config(
    executors=[
        IPyParallelExecutor(
            label='htcondor',
            provider=CondorProvider(
                channel=LocalChannel(),
                nodes_per_block=1,
                init_blocks=1,
                max_blocks=1,
                scheduler_options='accounting_group = group_sdcc.main',
                worker_init='',     # Input your worker_init if needed
                requirements='',  
            ),
            engine_debug_level='DEBUG',
        )
    ],
)

parsl.clear()
parsl.load(config)

@python_app()
def hello():
        return 'Hello World'

print(parsl.__version__)
print(hello().result())