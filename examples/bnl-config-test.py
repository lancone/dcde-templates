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
from dcdeparsl.configfactory import ConfigFactory



@python_app
def sdcc_wninfo():
    #import subprocess
    import os
    return os.uname()

#parsl.set_stream_logger(level=0)
parsl.clear()

cf = ConfigFactory()
bnl_sdcc_condor = cf.getconfig(site='bnl', user='dcde1000001')

parsl.load(bnl_sdcc_condor)

#condorinfo = sdcc_wninfo(executors=['sdcc_condor'])
condorinfo = sdcc_wninfo(stdout='relion_condor.out', stderr='relion_condor.err')

# Must. wait. for. job. to. finish.
condorinfo.result()

with open (condorinfo.stdout, 'r') as f:
    print(condorinfo.read())
