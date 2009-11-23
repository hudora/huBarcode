#!/usr/bin/env python
"""Example code for qrcode library"""
__revision__ = "$Revision$"

from qrcode import QRCodeEncoder
import sys
import logging

logging.getLogger("qrcode").setLevel(logging.DEBUG)
logging.getLogger("qrcode").addHandler(logging.StreamHandler(sys.stdout))

if __name__ == "__main__":
    ENCODER = QRCodeEncoder(sys.argv[1])
    ENCODER.save("test.png", 3)
    print ENCODER.get_ascii()
