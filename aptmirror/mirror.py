#!/usr/bin/env python3

import os, re, sys
import pathlib



import aptmirror.validate

"""
    This file contains everything for the mirror file/config handling
"""

class MirrorConfig( object ):

    def __init__( self, filename, **opt ):
        self._config = dict()
        self._filename = filename
        self._debug = False
        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

        cf = pathlib.Path( self._filename )
        if ! cf.exists():
            raise OSError("No such file %s" % ( self._filename ) )


if __name__ == "__main__":
    pass
