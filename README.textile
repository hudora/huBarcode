h1. huBarcode

huBarcode is a Python Library to generate 1D and 2D Barcodes. Currently it
supports

 * code128
 * ean13
 * datamatrix
 * qrcode


!https://raw.github.com/mdornseif/huBarcode/master/hubarcode/code128/test_img/3.png! !https://raw.github.com/mdornseif/huBarcode/master/hubarcode/ean13/test_img/3.png! !https://raw.github.com/mdornseif/huBarcode/master/sample_barcodes/hudora.png! !https://raw.github.com/mdornseif/huBarcode/master/hubarcode/qrcode/test_img/10.png!

The interface of the different encoders is fairly straightforward:

<pre><code>
>>> encoder = DataMatrixEncoder("HuDoRa")
>>> encoder.save( "test.png" )
>>> print encoder.get_ascii()
XX  XX  XX  XX  XX  XX  XX
XX  XXXX  XXXXXX      XXXXXX
XXXXXX    XX          XX
XXXXXX    XX        XXXX  XX
XXXX  XX  XXXXXX
XXXXXX    XXXXXXXX    XXXXXX
XX    XX  XXXXXXXX  XXXX
XX    XX      XXXX      XXXX
XX  XXXXXXXXXX    XXXX
XX  XXXX    XX            XX
XX  XXXXXX  XXXXXX      XX
XXXXXX  XX  XX  XX  XX    XX
XX    XX              XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXX
</code></pre>


h2. Download

You can get huBarcode at "the Python Cheeseshop":http://pypi.python.org/pypi/huBarcode/ or at "GitHub":http://github.com/mdornseif/huBarcode#.


h2. Decoders

Open Source barcode decoders we are aware of:

* "ZXing (Zebra Crossing)":http://code.google.com/p/zxing/ (higly recommended)
* "ExactCODE;":http://www.exactcode.de/site/open_source/exactimage/bardecode/
* "ZBar":http://sourceforge.net/projects/zbar/
* "pydmtx":http://libdmtx.wikidot.com/libdmtx-python-wrapper



h2. Changes

See the "Changelog":https://github.com/hudora/mdornseif/blob/master/CHANGES

h2. License

If you worry about copyright you might consider this Software BSD-Licensed.
If you are still worried, you might consider it GPL1/2/3 compatible.
But don't worry. If you need something formal:
The code is available under the Apache License, Version 2.0.


!https://travis-ci.org/hudora/huBarcode.png?branch=master!:https://travis-ci.org/hudora/huBarcode
