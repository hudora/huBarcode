#import ez_setup
#ez_setup.use_setuptools()
from distutils.core import setup

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
            
setup(name='huBarcode',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      url='http://www.hosted-projects.com/trac/hudora/public/wiki/huBarcode',
      version='0.6',
      description='generation of barcodes in Python',
      long_description='generation of various 2D barcodes (datamatrix and QR Code) in Python',
      license='BSD',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python',
                   'Topic :: Multimedia :: Graphics',
                   'Topic :: Office/Business'],
      keywords = "barcode datamatrix qrcode",
      
      install_requires = ['PIL>=1.1'],
      
      zip_safe = True,
      package_dir = {'huBarcode': ''},
      packages=['huBarcode', 'huBarcode.qrcode', 'huBarcode.qrcode.qrdata', 'huBarcode.datamatrix'],
      
)
