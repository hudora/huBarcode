#!/usr/bin/env python
# encoding: utf-8
"""
decode.py

Created by Maximillian Dornseif on 2007-06-28.
Copyright (c) 2007 HUDORA GmbH. All rights reserved.
"""

import sys
import os
import unittest
import Image
from operator import itemgetter
import code128encoding as encoding

def widths2bits(widths):
    """ Converts a list of widths into a list of bits.
    
    >>> widths2bits('21234')
    '110110001111'
    >>> widths2bits('01234')
    '1001110000'
    """
    
    ret = []
    statecount = 0
    for width in widths:
        if int(width): # ignore width == 0
            statecount += 1
        ret.append(str(statecount%2)*int(width))
    return ''.join(ret)

def bits2widths(rowbits):
    """Convert a stream of widths to a list of bits.
    
    >>> bits2widths('110110001111')
    '21234'
    >>> bits2widths('11010010000110001010001')
    '2112142311131'
    """
    ret = []
    state = rowbits[0]
    statelen = 0
    for bit in rowbits[1:]:
        statelen += 1
        if bit != state:
            ret.append(str(statelen))
            state = bit
            statelen = 0
    ret.append(str(statelen+1))
    return ''.join(ret)


def bits_to_values(rowbits):
    rowbits = rowbits.strip('0')
    #if len(rowbits) % 11 != 0:
    #    raise RuntimeError, "invalid bitstring %d %d %r" % (len(rowbits), len(rowbits)%11, rowbits)
    while rowbits:
        charbits = rowbits[:11]
        rowbits = rowbits[11:]
        v = encoding.encodings_rev.get(charbits)
        print repr((charbits, v, encoding.charset_a_rev.get(v), encoding.charset_b_rev.get(v), encoding.charset_c_rev.get(v)))

def rawhistogramm(rowbits):
    statecount = {}
    widths = bits2widths(rowbits)
    for width in widths:
        statecount[width] = statecount.get(width, 0) + 1
    return statecount


def normalizedhistogramm(rowbits):
    statecount = rawhistogramm(rowbits)
    top4widths = sorted(statecount.items(), key=itemgetter(1), reverse=True)[:4]
    minwidth = min([int(itemgetter(0)(x)) for x in top4widths])
    return [int(x)/minwidth for x in bits2widths(rowbits)][1:]


class EncodingTests(unittest.TestCase):
    # "HelloWorld!", encoded using "code 128"
    # The space/bar succession is represented by the following widths (space first):
    #02112142311131122142211142211141341113113211341111212412211141412212221221212232331112
    def test_basic(self):
        print bits_to_values(widths2bits('2112142311131122142211142211141341113113211341111212412211141412212221221212232331112'))

class DecodeHelloWorldTests(unittest.TestCase):
    # "HelloWorld!", encoded using "code 128"
    # The space/bar succession is represented by the following widths (space first):
    #02112142311131122142211142211141341113113211341111212412211141412212221221212232331112
    def setUp(self):
        pass
    
    def _get_middle_rowbits(self, filename):
        im = Image.open(filename).convert("1")
        row = im.size[1]/2
        # AND three lines to get arround dittering issues
        for col in range(im.size[0]):
            im.putpixel((col, row), im.getpixel((col, row)) \
                                     & im.getpixel((col, row + 1)) & im.getpixel((col, row + 2)) \
                                     & im.getpixel((col, row - 1)) & im.getpixel((col, row - 2)))
        im.show()
        return [int(im.getpixel((col, row)) == 0) for col in range(im.size[0])]
    
    def test_basic(self):
        rowbits = self._get_middle_rowbits('testdata/HelloWorld.png')
        hist = normalizedhistogramm(rowbits)
        self.assertEqual(''.join([str(x) for x in hist]),
                         '02112142311131122142211142211141341113113211341111212412211141412212221221212232331112')
    
    def test_basic_large(self):
        rowbits = self._get_middle_rowbits('testdata/HelloWorldLarge.png')
        
        widths = bits2widths(rowbits)
        self.assertEqual(rawhistogramm(rowbits), {5: 22, 6: 19, 11: 19, 12: 7, 16: 3, 17: 6, 22: 9, 56: 1})
        
        hist = normalizedhistogramm(rowbits)
        self.assertEqual(''.join([str(x) for x in hist]),
                         '02112142311131122142211142211141341113113211341111212412211141412212221221212232331112')
    
    
    #def test_basic_small(self):
    #    rowbits = self._get_middle_rowbits('testdata/HelloWorldSmall.png')
    #    hist = normalizedhistogramm(rowbits)
    #    self.assertEqual(''.join([str(x) for x in hist]),
    #                     '2112142311131122142211142211141341113113211341111212412211141412212221221212232331112')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()