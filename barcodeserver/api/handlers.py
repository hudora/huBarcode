#!/usr/bin/env python
# encoding: utf-8
"""
handlers.py

Created by Maximillian Dornseif on 2009-11-23.
Copyright (c) 2009 HUDORA. All rights reserved.
"""


import cStringIO
from code128 import Code128Encoder
from django.http import HttpResponse, HttpResponseRedirect

def code128_handler( request, barcodestr):
    barcodestr = barcodestr[:200]
    encoder = Code128Encoder(barcodestr)
    outfile = cStringIO.StringIO()
    encoder.save(outfile)
    response = HttpResponse(mimetype='image/png')
    response.write(outfile.getvalue())
    return response
    
