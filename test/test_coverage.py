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

import ean13.eantest
suite = unittest.TestLoader().loadTestsFromName('ean13.eantest.EAN13Test')
unittest.TextTestRunner().run(suite)

import code128.code128test
suite = unittest.TestLoader().loadTestsFromName('code128.code128test.Code128Test')
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
				 'ean13/__init__.py',
				 'ean13/encoding.py',
				 'ean13/renderer.py',
				 'code128/__init__.py',
				 'code128/encoding.py',
				 'code128/textencoder.py',
				 'code128/renderer.py'
                 ])
