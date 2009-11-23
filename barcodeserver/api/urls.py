#!/usr/bin/env python
# encoding: utf-8
"""
api/urls.py

Created by Maximillian Dornseif on 2009-11-23.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

from django.conf.urls.defaults import *
from piston.doc import documentation_view
from piston.resource import Resource
from huBarcode.barcodeserver.api.handlers import code128_handler

urlpatterns = patterns('',
   url(r'^code128/(?P<barcodestr>.*)', code128_handler, name='api_code128_handler'),
   # automated documentation
   # url(r'^$', documentation_view),
)