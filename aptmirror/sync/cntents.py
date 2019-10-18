#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.mirror.local


from pprint import pprint

class MirrorContents( object ):

    def __init__(self, mconf, **opt ):
        self._options = opt
        self._debug = False

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']



if __name__ == "__main__":
    pass
