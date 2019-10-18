#!/usr/bin/env python3
"""
    Handles checksum calcualtions
"""
import os, re, sys
import hashlib
from pprint import pprint
from pathlib import Path


DEFAULT_CHECKSUM="sha256"
WANTED_ALGORITHMS=("sha1", "sha256", "sha512", "md5")
################################################################################
## Hashing large files
################################################################################
class FileHash( object ):
    def __init__( self, filename, self._algorithm=DEFAULT_CHECKSUM, **opt ):
        self._debug = False
        self._blocksize = 65536
        self._algorithm = self._algorithm
        self._filename = filename

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

        if 'blocksize' in opt and int( opt['blocksize'] ) > 0:
            self._blocksize = int( opt['blocksize'] )

        if self._algorithm not in hashlib.algorithms_available():
            raise AttributeError("Unsupported hash algorithm: %s" % () )

    def hash( self ):
        hasher = None
        BLOCKSIZE = self._blocksize

        if self._algorithm in WANTED_ALGORITHMS:
            hasher = hashlib.new( self._algorithm )
        else:
            raise AttributeError("Unwanted hash algorithm: %s" % ( self._algorithm ) )

        with open( filename, 'rb') as f:
            buf = f.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(BLOCKSIZE)

        self._hash = hasher.hexdigest()
        return hasher.hexdigest()


if __name__ == "__main__":
    pass
