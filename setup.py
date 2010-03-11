long_description = """
huBarcode contains a collection of tools to generate various 1D and 2D barcvodes in Python.
"""

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
            
hubarcode = setup(name='huBarcode',
    maintainer='Maximillian Dornseif',
    maintainer_email='md@hudora.de',
    url='http://github.com/hudora/huBarcode',
    version='0.57',
    description='generation of barcodes in Python',
    long_description=long_description,
    classifiers=['License :: OSI Approved :: BSD License',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Multimedia :: Graphics',
                 'Topic :: Office/Business'],
    # download_url
    package_dir = {'huBarcode': ''},
    packages=find_packages(),
    zip_safe=False,
)
