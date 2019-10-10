#!/usr/bin/env python3

import os, re, sys
from pprint import pprint

import aptmirror.mirror
"""
    This file defines the external command execution,
    input from user via cli and the actual excution.
    I.e. main tool logic
"""

OPTIONS={}

class Runner( object ):

    def __init__( self, args, **opt ):
        self._args = args
        self._debug = False
        self._mirror_config = None

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


    def run( self ):
        if len( self._args ) > 1:
            self._mirror_config = aptmirror.mirror.MirrorConfig( self._args[1] )
            pprint( self._mirror_config.get_config() )
            pprint( self._mirror_config.get_mirrors() )
            for m in self._mirror_config.get_mirrors():
                pprint( m.get_index_links() )

    def get_options( ):
        return "<mirror.list>"

if __name__ == "__main__":
    pass
