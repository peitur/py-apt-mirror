#!/usr/bin/env python3

import os, re, sys

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
        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def run( self ):
        pass

    def get_options( ):
        return "<mirror.list>"

if __name__ == "__main__":
    pass
