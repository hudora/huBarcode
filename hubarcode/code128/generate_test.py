"""Generate test images for code128 barcode encoder"""

__revision__ = "$Rev: 1$"

from __init__ import Code128Encoder
from code128test import Code128Test

for index, string in enumerate(Code128Test.test_strings):
    enc = Code128Encoder(string)
    enc.save("code128/test_img/%d.png" % (index+1) )
