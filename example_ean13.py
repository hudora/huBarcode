"""Example code for ean13 library"""
__revision__ = "$Revision$"

from ean13 import EAN13Encoder
import sys
import logging

logging.getLogger("ean13").setLevel(logging.DEBUG)
logging.getLogger("ean13").addHandler(logging.StreamHandler(sys.stdout))

if __name__ == "__main__":
    encoder = EAN13Encoder( sys.argv[1] )
    encoder.save( "test.png" )
