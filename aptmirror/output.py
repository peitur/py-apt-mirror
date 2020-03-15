#!/usr/bin/env python3

import os, re, sys
import logging

import aptmirror.frmt as frmt


"""
    Handles output stuff
"""

class Output( object ):

    def __init__( self, **opt ):
        self._debug = False
        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

if __name__ == "__main__":
    pass
