#!/usr/bin/env python3
"""
    Handles locking of mirrors
"""

import os, re, sys
import pathlib
import datetime
import time

from pprint import pprint

LOCK_FILENAME=".lock"

class MirrorLock( object ):

    def __init__( self, varpath, lockfile=LOCK_FILENAME, **opt ):
        self._debug = False
        self._options = opt
        self._path = varpath
        self._filename = lockfile
        self._lockfile = "%s/%s" % ( self._path, self._filename )

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def lock( self ):
        if not self.is_locked():
            pathlib.Path( self._lockfile ).touch()

    def unlock( self ):
        if self.is_locked():
            pathlib.Path( self._lockfile ).unlink()

    def is_locked( self ):
        return pathlib.Path( self._lockfile ).exists()

    def lock_age( self ):
        if not self.is_locked():
            raise RuntimeError("Lock missing: %s" % ( self._lockfile ) )

        return int( ( datetime.datetime.now() - datetime.datetime.fromtimestamp( pathlib.Path( self._lockfile ).stat().st_mtime ) ).total_seconds() )




if __name__ == "__main__":
    pass
