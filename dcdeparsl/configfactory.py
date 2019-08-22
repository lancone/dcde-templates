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
import requests

class ConfigFactory(object):

    def __init__(self, conffile='/etc/dcde/dcdeparsl.conf'):
        self.log = logging.getLogger()
        self.conffile = conffile
        self.config = configparser.ConfigParser()
        self.config.read(self.conffile)
        self.clienthostname = socket.gethostname()
        try:
            f = requests.request('GET', 'http://whatismyip.org')            
            self.external_ip = f.text
            # urllib2.urlopen('http://whatismyip.org').read()
        except:
            self.log.warning("external ip lookup failed. ")
        
        self.ipaddress = socket.gethostbyname(self.clienthostname)    
        self.log.debug("ConfigFactory created. clienthostname=%s external_ip=%s" % (self.clienthostname, 
                                                                                    self.external_ip))

    def getconfig(self, endpoint, user):
        '''
        Generate valid parsl Config object given endpoint and user. 
        '''
        worker_port_range_low = int(self.config.get('client', 'worker_port_range_low'))
        worker_port_range_high = int(self.config.get('client', 'worker_port_range_high'))
        homeroot = self.config.get(endpoint, 'homeroot')
        worker_init = self.config.get(endpoint, 'worker_init')
        install_user = self.config.get(endpoint, 'install_user')
        channel_port = int(self.config.get(endpoint, 'channel_port') )
        scheduler_options = self.config.get(endpoint, 'scheduler_options')
        batch = self.config.get(endpoint, 'batch')

        self.log.debug("Got channel parameters: endpoint=%s user=%s channel_port=%s script_dir=%s homeroot=%s " % (endpoint, 
                                                                                                                   user, 
                                                                                                                   channel_port,
                                                                                                                   '%s/%s/parsl_scripts'% (homeroot, user),
                                                                                                                   homeroot))
        self.log.debug("Got provider parameters: batch=%s scheduler_options=%s worker_init=%s " % (batch,
                                                                                                   scheduler_options,
                                                                                                   worker_init))
        
        self.log.debug("Got executor parameters: port_high=%s port_low=%s " % (worker_port_range_low, 
                                                                               worker_port_range_high,
                                                                               ))
        
        config = None
        myprovider = None
        
        mychannel=OAuthSSHChannel(
            hostname=endpoint,
            port=channel_port,
            username=user,     # Please replace USERNAME with your username
            script_dir='%s/%s/parsl_scripts'% (homeroot, user) ,    # Please replace USERNAME with your username
        )

        if batch == 'htcondor':
            self.log.debug("batch type is %s" % batch)
            myprovider=CondorProvider(
                channel = mychannel,
                #nodes_per_block=1,
                init_blocks=1,
                #max_blocks=4,
                scheduler_options=scheduler_options,
                worker_init=worker_init,     # Input your worker_init if needed,
            )
            
        elif batch == 'slurm':
            self.log.debug("batch type is %s" % batch)        
            myprovider=SlurmProvider(
                channel = mychannel,
                #nodes_per_block=1,
                init_blocks=1,
                #max_blocks=4,
                scheduler_options=scheduler_options,
                worker_init=worker_init,     # Input your worker_init if needed,
            )        
        

        config = Config(
            executors=[
                        HighThroughputExecutor(
                                address=self.external_ip,
                                worker_port_range=(worker_port_range_low,worker_port_range_high),
                                label='condor_oauth_ssh',
                                worker_debug=True,
                                worker_logdir_root='%s/%s/parsl_scripts/logs' % (homeroot, user),
                                working_dir='%s/%s/parsl_scripts' % (homeroot, user),
                                provider = myprovider,
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
    
    