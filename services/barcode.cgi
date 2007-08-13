#!/usr/local/bin/python
# encoding: utf-8
"""
barcode.cgi - A CGI script that generates barcodes as PNG image.
Available parameters:
- value: the value that should be encoded
- encoding: example: EAN8, EAN13
- width, height: width, height of barcode image
"""

# Installation:
# reportlab 2
# python/site-packages/reportlab/fonts auffuellen mit:
#    reportlab: http://bioinf.scri.ac.uk/lp/downloads/programs/genomediagram/pfbfer.zip
# PIL 
# renderPM: http://www.reportlab.co.uk/svn/public/reportlab/trunk/rl_addons/renderPM/

import sys
import cgi
import reportlab.graphics.barcode as barcode

if __name__ == "__main__":
    form = cgi.FieldStorage()
    if not form.has_key('code'):
        sys.stdout.write("Content-Type: text/text\n\n")
        sys.stdout.write("ERROR")
        sys.exit(1)

    code = form.getvalue('code')
    encoding = form.getvalue('encoding', 'EAN13')
    width = form.getvalue('width', None)
    if width:
         width = int(width)

    height = form.getvalue('height', None)
    if height:
         height = int(height)

    b = barcode.createBarcodeDrawing(encoding, value=code, width=width, height=height)
    sys.stdout.write("Content-Type: image/png\n\n")
    sys.stdout.write(b.asString('png'))
