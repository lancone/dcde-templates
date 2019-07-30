#!/bin/evn python
#
# Simple test of the Oauth channel standalone from parsl
# @author: maheshwarikc@ornl.gov

import parsl
from parsl.channels import OAuthSSHChannel

def test_channel():
    channel = OAuthSSHChannel(hostname='spce01.sdcc.bnl.gov', port=2222, username='dcde1000005')
    x, stdout, stderr = channel.execute_wait('ls')
    print(x, stdout, stderr)
    assert x == 0, "Expected exit code 0, got {}".format(x)

if __name__ == '__main__':
    test_channel()
    