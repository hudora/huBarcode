#!/usr/bin/env python
"""Coverage and unittest for datamatrix and QR Code library"""
__revision__ = "$Revision$"

import sys, unittest
sys.path.append('.')
import coverage # get it from http://www.nedbatchelder.com/code/modules/coverage.html

coverage.erase()
coverage.start()

import qrcode.qrcodetest
suite = unittest.TestLoader().loadTestsFromName('qrcode.qrcodetest.MatrixTest')
unittest.TextTestRunner().run(suite)

import datamatrix.matrixtest
suite = unittest.TestLoader().loadTestsFromName('datamatrix.matrixtest.MatrixTest')
unittest.TextTestRunner().run(suite)


coverage.stop()
coverage.report(['qrcode/__init__.py',
                 'qrcode/isodata.py',
                 'qrcode/qrcodetest.py',
                 'qrcode/renderer.py',
                 'qrcode/textencoder.py',
                 'datamatrix/__init__.py',
                 'datamatrix/placement.py',
                 'datamatrix/renderer.py',
                 'datamatrix/reedsolomon.py',
                 'datamatrix/textencoder.py',
                 ])
                            