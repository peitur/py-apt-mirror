#!/usr/bin/env python3

import os, re, sys

"""
    This file defines the external command execution,
    input from user via cli and the actual excution.
    I.e. main tool logic
"""

class Runner( object ):

    def __init__( self, **opt ):
        self._debug = False
        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


if __name__ == "__main__":
    pass
