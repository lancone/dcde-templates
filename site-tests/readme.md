This `site-tests` subdirectory contains simple python scripts that are meant to
test connectivity and basic parsl functionality to each DCDE compute site.   

Each consists of a parsl config that should submit a batch job from the BNL DCDE Jupyterhub (https://jupyter05.sdcc.bnl.gov:8000/),
and provide a little bit of information from a worker node at that site.  This
simple test must work and return the data from the remote worker node in order
for our planned DCDE demo to work.

The big challenge seems to be to get all of the network  connections (specified
by the port ranges in the config) plumbed to the remote site and back.  There
are many obstacles: sites block ports incoming and outgoing for a variety of
reasons, so network and firewall configs and these parsl configs need to be
aligned so the data can thread the needle(s) to the remote sites and back.

All of these tests use the parsl HighThroughputExecutor, which sets up an "interchange" on the local machine (i.e. the BNL jupyterhub) to communicate with the (remote) compute cluster to submit jobs and pass the results back.  This
local interchange mode may not be the best way for DCDE to use parsl. Yadu
Babuji of the parsl team has suggested we might want to use the remote_executor
branch of the parsl codebase.

Yadu's comment from Slack this morning:

> Hi David, the remote_interchange branch solves the issue of compute nodes not being able to connect out to the internet, by launching the interchange on the login nodes which are usually reachable from the compute nodes. This might not be necessary if your compute nodes have outbound connectivity...  Yes you would need it on all the remote clusters, since the interchange is instantiated from the cluster-local environment.

I can clone the remote_interchange branch with this command:
`git clone --single-branch --branch remote_interchange https://github.com/Parsl/parsl.git`

I have *not* tried to use that branch, it would need (as Yadu mentions above) to be installed on all our DCDE clusters if we were to use it.

Reference documentation on parsl configs is here: https://parsl.readthedocs.io/en/latest/reference.html
Documentation on the parsl execution model and its parts/pieces is here: https://parsl.readthedocs.io/en/latest/userguide/execution.html
Configuration examples for various sites are here:  https://parsl.readthedocs.io/en/latest/userguide/configuring.html
