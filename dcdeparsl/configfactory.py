#
# DCDE Parsl Config factory. Creates usable site-specific Parsl configuration object based 
# on dynamic input and configured defaults. 
# @author John Hover <jhover@bnl.gov>


import configparser
import logging
import socket
import parsl
from parsl.executors.ipp_controller import Controller
from parsl.channels.oauth_ssh.oauth_ssh import OAuthSSHChannel
from parsl.providers.condor.condor import CondorProvider
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.app.app import python_app, bash_app



bnl={
        "spce01.sdcc.bnl.gov": {
            "worker_port_range_low" : 50000,
            "worker_port_range_high" : 51000,
            "homeroot" : "/sdcc/u/",
            "worker_init" : "/sdcc/u/dcde1000001/setup.sh"
        }
    }


def getconfig(site, host, config=None):
    '''
    
    '''
    hostname = socket.gethostname()    
    ipaddress = socket.gethostbyname(hostname)    
    print(hostname)
    
    
    config = Config(
        executors=[
                    HighThroughputExecutor(
                            address=hostname,
                            worker_port_range=(50000,51000),
                            label='condor_oauth_ssh',
                            worker_debug=True,
                            worker_logdir_root='/sdcc/u/dcde1000001/parsl_scripts/logs',
                            working_dir='/sdcc/u/dcde1000001/parsl_scripts',
                            provider=CondorProvider(
                                    channel=OAuthSSHChannel(
                                            hostname='spce01.sdcc.bnl.gov',
                                            port=2222,
                                            username='dcde1000001',     # Please replace USERNAME with your username
                                            script_dir='/sdcc/u/dcde1000001/parsl_scripts',    # Please replace USERNAME with your username
                                    ),
                                    #nodes_per_block=1,
                                    init_blocks=1,
                                    #max_blocks=4,
                                    scheduler_options='accounting_group = group_sdcc.main',
                                    worker_init='source ~/setup.sh',     # Input your worker_init if needed,
                            ),
                    )
            ],
    )