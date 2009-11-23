"""Example code for datamatrix library"""
__revision__ = "$Revision$"

from datamatrix import DataMatrixEncoder
import sys
import logging

logging.getLogger("datamatrix").setLevel(logging.DEBUG)
logging.getLogger("datamatrix").addHandler(logging.StreamHandler(sys.stdout))

if __name__ == "__main__":
    encoder = DataMatrixEncoder( sys.argv[1] )
    encoder.save( "test.png" )
    print encoder.get_ascii( )
