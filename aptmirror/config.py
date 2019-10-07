#!/usr/bin/env python3

import os, re, sys

"""
    Contains handling of main tool configuration
"""

class ToolConfig( object ):

    def __init__( self, filename, **opt ):
        self._debug = False
        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


if __name__ == "__main__":
    pass
