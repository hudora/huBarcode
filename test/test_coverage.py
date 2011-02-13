#!/usr/bin/env python
"""Coverage and unittest for datamatrix and QR Code library"""

import sys
import unittest

import coverage # get it from http://www.nedbatchelder.com/code/modules/coverage.html

exitcode = 0

coverage.erase()
coverage.start()

import hubarcode.qrcode.qrcodetest
suite = unittest.TestLoader().loadTestsFromName('qrcode.qrcodetest.MatrixTest')
results = unittest.TextTestRunner().run(suite)
if not results.wasSuccessful():
    exitcode += 1

import hubarcode.datamatrix.matrixtest
suite = unittest.TestLoader().loadTestsFromName('datamatrix.matrixtest.MatrixTest')
results = unittest.TextTestRunner().run(suite)
if not results.wasSuccessful():
    exitcode += 1

import hubarcode.ean13.eantest
suite = unittest.TestLoader().loadTestsFromName('ean13.eantest.EAN13Test')
results = unittest.TextTestRunner().run(suite)
if not results.wasSuccessful():
    exitcode += 1

import hubarcode.code128.code128test
suite = unittest.TestLoader().loadTestsFromName('hubarcode.code128.code128test.Code128Test')
results = unittest.TextTestRunner().run(suite)
if not results.wasSuccessful():
    exitcode += 1

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

sys.exit(exitcode)
