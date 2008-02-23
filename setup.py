from distutils.core import setup

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
      url='http://www.hosted-projects.com/trac/hudora/public/wiki/huBarcode',
      version='0.51',
      description='generation of barcodes in Python',
      classifiers=['License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python',
                   'Topic :: Multimedia :: Graphics',
                   'Topic :: Office/Business'],
      # download_url
      package_dir = {'huBarcode': ''},
      packages=['huBarcode', 'huBarcode.qrcode', 'huBarcode.qrcode.qrcode_data', 'huBarcode.datamatrix', 'huBarcode.ean13', 'huBarcode.code128'],
      zip_safe=False,
)

from distutils import dir_util,file_util
import sys, os

# from http://www.redbrick.dcu.ie/~noel/distutils.html
# copy fonts into install dir
if "install" in sys.argv:
    wheretoinstall = hubarcode.command_obj['install'].install_purelib
    dir_util.copy_tree('fonts',os.path.join(wheretoinstall,'huBarcode','fonts'))

