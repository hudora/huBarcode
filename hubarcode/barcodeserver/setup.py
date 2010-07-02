#!/usr/bin/env python
# encoding: utf-8
"""barcodeserver is xXXXx
"""

# setup.py
# Created by Maximillian Dornseif on 2009-11-23 for HUDORA.
# Copyright (c) 2009 HUDORA. All rights reserved.

__revision__ = '$Revision: 6862 $'

from setuptools import setup, find_packages

setup(name='barcodeserver',
      maintainer='Maximillian Dornseif',
      # maintainer_email='xXXXx@hudora.de',
      version='1.0',
      description='xXXXx FILL IN HERE xXXXx',
      long_description=__doc__,
      classifiers=['License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python'],
      download_url='https://cybernetics.hudora.biz/nonpublic/eggs/',
      package_data={"barcodeserver": ["templates/barcodeserver/*.html", "reports/*.jrxml", "bin/*"]},
      packages=find_packages(),
      include_package_data=True,
      install_requires=['huTools', 'huDjango'],
      dependency_links = ['http://cybernetics.hudora.biz/dist/',
                          'http://cybernetics.hudora.biz/nonpublic/eggs/'],
)
