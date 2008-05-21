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
    url='https://cybernetics.hudora.biz/projects/wiki/huBarcode',
    version='0.52',
    description='generation of barcodes in Python',
    long_description=long_description,
    classifiers=['License :: OSI Approved :: BSD License',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Multimedia :: Graphics',
                 'Topic :: Office/Business'],
    # download_url
    package_dir = {'huBarcode': ''},
    packages=['huBarcode', 'huBarcode.qrcode', 'huBarcode.qrcode.qrcode_data', 
              'huBarcode.datamatrix', 'huBarcode.ean13', 'huBarcode.code128'],
    data_files=[('fonts', ['fonts/cour.pbm', 'fonts/cour.pil', 'fonts/courR08.pbm', 'fonts/courR08.pil',
                           'fonts/courR10.pbm', 'fonts/courR10.pil', 'fonts/courR12.pbm',
                           'fonts/courR12.pil', 'fonts/courR14.pbm', 'fonts/courR14.pil',
                           'fonts/courR18.pbm', 'fonts/courR18.pil', 'fonts/courR24.pbm',
                           'fonts/courR24.pil'])],
    zip_safe=False,
)
