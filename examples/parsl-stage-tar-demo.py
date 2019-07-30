#!/usr/bin/env python3

"""

Example:  stage a tarfile from a remote Globus endpoint to SDCC BNL endpoint
and list it out using a PARSL app

prerequisites:
    Globus credential (likely obtained by running parsl-globus-auth)
    Activated Globus endpoints

See the local site-packages/parsl/data_provider/globus.py
for the apparently undocumented Globus storage provider.

"""

import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import Config
from parsl.data_provider.files import File
from parsl.data_provider.scheme import GlobusScheme
from parsl.executors.threads import ThreadPoolExecutor


#print(parsl.__version__)

@bash_app
def tar_list(tarfile, stdout='taroutput.txt'):
    # note we send output to stdout.txt, but don't do anything with it!
    bashcmd = '/usr/bin/tar tfz {}'.format(tarfile)
    return(bashcmd)


# Specify the config for the machine the data will land on, particularly the
# Globus endpoint by UUID within the storage_access construct:
config = Config(
    executors=[
        ThreadPoolExecutor(
            label='local_threads_globus',
            working_dir='/sdcc/u/dcde1000006/globus-scratch',
            storage_access=[GlobusScheme(
                endpoint_uuid='23f78cc8-41e0-11e9-a618-0a54e005f950'
            )],
        )
    ],
)


parsl.clear()
parsl.load(config)

# Try a trivial staging exercise, pulling this file if it's not already available:
# Note this is not a public file!  You probably want to find one you can read.
tarfile = File('globus://e133a52e-6d04-11e5-ba46-22000b92c6ec/archive/d3c724/bbcp.tar.Z')

f = tar_list(tarfile)

# Block while we wait for the app to finish:
f.result()

with open (f.stdout, 'r') as tarout:
    print (tarout.read())
