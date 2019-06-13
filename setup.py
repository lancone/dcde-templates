#
# Basic setup file for pip install
#

import os
import sys
from setuptools import setup, find_packages

#example_files = ['examples/%s' %file for file in os.listdir('examples') if os.path.isfile('examples/%s' %file) ]

setup(
    name="dcde-templates",
    version='0.90',
    description='Python Libraries for DCDE usage.',
    long_description='''Python Libraries for DCDE usage.''',
    license='BSD',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='https://github.com/bnl-sdcc/dcde-templates',
    #python_requires='>=2.7',
    packages=[ 'dcdeparsl',
               'dcdeexamples',
               ],
    install_requires=[],
    
    data_files=[
        # examples
        #('/usr/share/dcde', example_files
        # ),        
        ],
    )


