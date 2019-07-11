#!/bin/env python
#
# @author Ketan Maheshwari <maheshwarikc@ornl.gov>
#


import parsl
from parsl.app.app import bash_app
print(parsl.__version__) # We expect 0.7.2 for this notebook


# Load the right configs. We'll need updated configs and dev work to support Summit.

# The following is a config for Cori, that might be useful in porting over for the relion usecase
# We might need a bit of handholding here due to the presence of MPI applications.
# In parsl a block is a single unit that we request, so it maps to a single scheduler job
# In this case, we would specify the nodes_per_block as 2X the number of relion mpi tasks we
# can reasonably run.

"""

num_concurrent_relion_tasks_per_block = 2

from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.channels import SSHInteractiveLoginChannel
from parsl.providers import SlurmProvider

config = Config(
    executors=[
        HighThroughputExecutor(
            # We use this to limit the # of workers, and therefore the # of invocations of the mpi task per job
            max_workers=num_concurrent_relion_tasks_per_block,
            label="cori",
            worker_debug=False,
            address='try.parsl-project.org',
            interchange_address='cori03-224.nersc.gov',
            provider=SlurmProvider(
                partition='debug',  # Replace with partition name
                channel=SSHInteractiveLoginChannel(
                    hostname='cori03-224.nersc.gov',
                    username='yadunand',                         # MUST SET PER USER
                    script_dir='/global/homes/y/yadunand/parsl_scripts',
                ),
                init_blocks=1, # Number of blocks to start with
                min_blocks=1,  # Minimum # of blocks to maintain
                node_per_block=2 * num_concurrent_relion_tasks_per_block,
                # scheduler_options="#SBATCH --constraint=knl,quad,cache",
                scheduler_options="#SBATCH --constraint=haswell",
                worker_init='source ~/setup_parsl_0.7.2.sh',
            ),
            working_dir='/global/homes/y/yadunand',
            storage_access=[GlobusScheme(
                endpoint_uuid='9d6d99eb-6d04-11e5-ba46-22000b92c6ec',
                endpoint_path='/',
                local_path='/')],
        )]
)
"""

# THIS IS ONLY A PLACEHOLDER CONFIG TO GET THIS QUICKLY TESTED

# Try running with local_threads and mock=True to see how the bash app works
from parsl.configs.local_threads import config

# Alternative config for Cori Slurm system:
max_concurrent_tasks = 10
parsl.load(config)


# The bash_app will run on a worker node
@bash_app
def relion_refine_mpi(job_dir=None, stdout=None, stderr=None, mock=False):
    """
    Parameters
    ----------
    mock : (Bool)
       when mock=True
    """
    cmd_line = '''
export PATH=$PATH:/home/cades/relion/build/bin
export DATAROOT=/home/cades/relion21_tutorial/PrecalculatedResults || exit

if [ ! -d ./class3d ] ; then
  mkdir ./class3d || exit
fi

ln -sf /home/cades/relion21_tutorial/PrecalculatedResults/Extract Extract || exit

# This can help with debugging:
echo
echo "printenv output:"
echo
printenv
echo
echo "ldd -r output:"
echo
ldd -r `which relion_refine_mpi`

set -v

mpirun -n 2 `which relion_refine_mpi`  \
 --o class3d \
 --i /home/cades/relion21_tutorial/PrecalculatedResults/Select/after_sorting/particles.star \
 --ref /home/cades/relion21_tutorial/PrecalculatedResults/InitialModel/symC1/inimodel_symD2.mrc \
 --ini_high 50 \
 --dont_combine_weights_via_disc \
 --preread_images  \
 --pool 3 \
 --ctf \
 --ctf_corrected_ref \
 --iter 4 \
 --tau2_fudge 4 \
 --particle_diameter 200 \
 --K 4 \
 --flatten_solvent \
 --zero_mask \
 --oversampling 1 \
 --healpix_order 2 \
 --offset_range 5 \
 --offset_step 2 \
 --sym C1 \
 --norm \
 --scale  \
 --j 1

set +v
    '''
    if mock:
        return '''tmp_file=$(mktemp);
cat<<EOF > $tmp_file
{}
EOF
cat $tmp_file
        '''.format(cmd_line)
    else:
        return cmd_line



if __name__ == "__main__":

    # Call Relion and wait for results
    x = relion_refine_mpi(stdout="relion.out", stderr="relion.err")
    x.result()

    with open(x.stdout, 'r') as f:
        print(f.read())
        
        
