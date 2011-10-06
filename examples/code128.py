"""Example code for code128 library"""


import logging
import sys
from hubarcode.code128 import Code128Encoder

logging.getLogger("code128").setLevel(logging.DEBUG)
logging.getLogger("code128").addHandler(logging.StreamHandler(sys.stdout))

if __name__ == "__main__":
    encoder = Code128Encoder(sys.argv[1])
    encoder.save("test.png")
