#!/bin/env python3
#
# Remote Condor via SSH channel
# DOES NOT WORK WITH GSISSH yet. no port. Uses paramiko
#
import parsl
from parsl.executors.ipp_controller import Controller
from parsl.channels.oauth_ssh.oauth_ssh import OAuthSSHChannel
from parsl.providers.condor.condor import CondorProvider
from parsl.config import Config
from parsl.executors.ipp import IPyParallelExecutor
from parsl.app.app import python_app, bash_app

config = Config(
    executors=[
        IPyParallelExecutor(
            label='condor_oauth_ssh',
            provider=CondorProvider(
                channel=OAuthSSHChannel(
                    hostname='spce01.sdcc.bnl.gov',
                    port=2222,
                    username='dcde1000001',     # Please replace USERNAME with your username
                    script_dir='/usatlas/u/dcde1000001/parsl_scripts',    # Please replace USERNAME with your username
                ),
                nodes_per_block=1,
                init_blocks=4,
                max_blocks=4,
                scheduler_options='accounting_group = group_sdcc.main',
                worker_init='',     # Input your worker_init if needed
            ),
            controller=Controller(public_ip='130.199.16.40'),    # Please replace PUBLIC_IP with your public ip
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