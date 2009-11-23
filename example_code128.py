"""Example code for code128 library"""
__revision__ = "$Revision: 1$"

from code128 import Code128Encoder
import logging, sys

logging.getLogger("code128").setLevel(logging.DEBUG)
logging.getLogger("code128").addHandler(logging.StreamHandler(sys.stdout))

if __name__ == "__main__":
    encoder = Code128Encoder( sys.argv[1] )
    encoder.save( "test.png" )
