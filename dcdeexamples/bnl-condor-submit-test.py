#!/usr/bin/env python3

import parsl
from parsl.app.app import python_app, bash_app
from parsl.executors.ipp_controller import Controller
#from parsl.channels.ssh.ssh import SSHChannel
from parsl.channels.local.local import LocalChannel
#from parsl.providers.condor import condor
from parsl.providers import CondorProvider
from parsl.config import Config
#from parsl.executors.ipp import IPyParallelExecutor
from parsl.executors import HighThroughputExecutor

@python_app
def sdcc_wninfo():
    #import subprocess
    import os
    return os.uname()

#parsl.set_stream_logger(level=0)
parsl.clear()

"""
Note 6/26/2019 DE Cowley: The config below in this comment kind of works,  in
that it gets jobs submitted to the condor queue.   however, output seems to go
nowhere, and jobs continually  resubmit.

An error appears in parsl.log:

1 job(s) submitted to cluster 1672. STDERR:
2019-06-26 19:27:38.879 parsl.executors.ipp:242 [DEBUG]  Launched block 0:1672.0
2019-06-26 19:27:38.879 parsl.executors.ipp:249 [ERROR]  No execution provider available
2019-06-26 19:27:38.880 parsl.executors.ipp:132 [DEBUG]  Starting executor


bnl_sdcc_condor = Config(
    executors=[
        IPyParallelExecutor(
            label='sdcc_condor',
            provider=CondorProvider(
                channel=LocalChannel(
                    script_dir='parsl_scriptdir'
                ),
                nodes_per_block=1,
                init_blocks=1,
                min_blocks=1,
                max_blocks=1,
                parallelism=0,
                scheduler_options='accounting_group = group_sdcc.main'
            ),
            workers_per_node=1,
            managed=False
        )
    ],
)

"""

"""
6/26/19 PM: try HTEX instead of ipyparallel (see below)

This produces an error in stdout from parsl:
parsl.parsl.auto.1561593082.171704.script: line 7: process_worker_pool.py: command not found

corresponding line in the submitted script:

process_worker_pool.py   -c 1.0 --poll 10 --task_url=tcp://130.199.185.13:54772 --result_url=tcp://130.199.185.13:54295 --l

"""

bnl_sdcc_condor = Config(
    executors=[
        HighThroughputExecutor(
            label='sdcc_condor',
            provider=CondorProvider(
                channel=LocalChannel(
                    script_dir='parsl_scriptdir'
                ),
                nodes_per_block=1,
                init_blocks=1,
                min_blocks=1,
                max_blocks=1,
                parallelism=0,
                scheduler_options='accounting_group = group_sdcc.main'
            ),
            address='130.199.185.13',
            managed=False
        )
    ],
)


parsl.load(bnl_sdcc_condor)

"""
try doing something more explicit with stderr and stdout (based on Ketan's
Cori/relion example):
"""

#condorinfo = sdcc_wninfo(executors=['sdcc_condor'])
condorinfo = sdcc_wninfo(stdout='relion_condor.out', stderr='relion_condor.err')

# Must. wait. for. job. to. finish.
condorinfo.result()

with open (condorinfo.stdout, 'r') as f:
    print(condorinfo.read())
