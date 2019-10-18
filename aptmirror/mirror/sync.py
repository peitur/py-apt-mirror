#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.validate
import aptmirror.utils
import aptmirror.checksum
import aptmirror.url

import aptmirror.mirror.local


from pprint import pprint

class MirrorSync( object ):

    def __init__(self, mconf, **opt ):
        self._options = opt
        self._debug = False
        self._mirror_config = mconf

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']



if __name__ == "__main__":
    pass
