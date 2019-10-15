#!/usr/bin/env python3

import os, re, sys
import tarfile, zipfile, bz2
import random, string
import json
import pathlib

from pprint import pprint

def is_type( o, t ):
    if type( o ).__name__ == t:
        return True
    return False

def random_string( length ):
    return ''.join(random.SystemRandom().choice( string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range( length ))


def size_htob( s ):
    rx = re.compile( r"([0-9\.]+)([bkMG]*)[bB]*" )
    m = rx.match( s )
    nbytes = None

    if m:
        amount = m.group(1)
        unit = m.group(2)

        if unit == "k":
            nbytes = int( float( amount ) * 1024 )
        elif unit == "M":
            nbytes = int( float( amount ) * 1024 * 1024 )
        elif unit == "G":
            nbytes = int( float( amount ) * 1024 * 1024 * 1024 )
        else:
            if re.match( r"[0-9]+\.[0-9]+", amount ):
                raise AttributeError("Bad byte format. Got float value!")
            nbytes = int( amount )
    return int( nbytes )


def size_btoh( s ):

    units = { "": 1, "k": 1024, "M": 1024 * 1024, "G": 1024 * 1024 * 1024  }

    x = int( s )
    for i in units:
        c = float( x / units[i] )
        if c < 500:
            return "%s%s" % ( c, i )
    return x


if __name__ == "__main__":
    pass
