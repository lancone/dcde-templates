#!/bin/env python
# DCDE Parsl Config factory. Creates usable site-specific Parsl configuration object based 
# on dynamic input and configured defaults. 
# @author John Hover <jhover@bnl.gov>

import argparse
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


class ConfigFactory(object):

    def __init__(self, conffile='/etc/dcde/dcdeparsl.conf'):
        self.conffile = conffile
        self.config = configparser.ConfigParser()
        self.config.read(self.conffile)
        self.clienthostname = socket.gethostname()            
        self.ipaddress = socket.gethostbyname(self.clienthostname)    
        self.log = logging.getLogger()
        self.log.debug("ConfigFactory created.")

    def getconfig(self, endpoint, user):
        '''
        Generate valid parsl Config object given endpoint and user. 
        '''
        worker_port_range_low = self.config.get(endpoint, 'worker_port_range_low')
        worker_port_range_high = self.config.get(endpoint, 'worker_port_range_high')
        homeroot = self.config.get(endpoint, 'homeroot')
        worker_init = self.config.get(endpoint, 'worker_init')
        
        config = Config(
            executors=[
                        HighThroughputExecutor(
                                address=self.clienthostname,
                                worker_port_range=(50000,51000),
                                label='condor_oauth_ssh',
                                worker_debug=True,
                                worker_logdir_root='/sdcc/u/dcde1000001/parsl_scripts/logs',
                                working_dir='/sdcc/u/dcde1000001/parsl_scripts',
                                provider=CondorProvider(
                                        channel=OAuthSSHChannel(
                                                hostname=endpoint,
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
        
        return config

    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "ConfigFactory: conffile=%s " % self.conffile    

    
    
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s (UTC) [%(levelname)s] %(name)s %(filename)s:%(lineno)d %(funcName)s(): %(message)s')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conffile', 
                        action="store", 
                        dest='conffile', 
                        default="/etc/dcde/dcdeparsl.conf",
                        help='configuration file.')

    parser.add_argument('-u', '--username', 
                        action="store", 
                        dest='username', 
                        default="dcde1000001",
                        help='remote username')

    
    parser.add_argument('-d', '--debug', 
                        action="store_true", 
                        dest='debug', 
                        help='debug logging')
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    log = logging.getLogger()
       
    cf = ConfigFactory(conffile=args.conffile)
    log.debug("ConfigFactory generated: %s" % cf)
    pcf = cf.getconfig( 'spce01.sdcc.bnl.gov', args.username)
    #print(pcf)
    
    