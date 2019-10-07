#!/usr/bin/env python3
"""
    Handles checksum calcualtions
"""
import os, re, sys
import hashlib
from pprint import pprint
from pathlib import Path


DEFAULT_CHECKSUM="sha256"

################################################################################
## Hashing large files
################################################################################
class FileHash( object ):
    def __init__( self, filename, chksum=DEFAULT_CHECKSUM, **opt ):
        self._debug = False
        self._blocksize = 65536
        self._algorithm = chksum
        self._filename = filename

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

        if 'blocksize' in opt and int( opt['blocksize'] ) > 0:
            self._blocksize = int( opt['blocksize'] )


    def hash( self ):
        BLOCKSIZE = self._blocksize

        if chksum == "sha1":
            hasher = hashlib.sha1()
        elif chksum == "sha224":
            hasher = hashlib.sha224()
        elif chksum == "sha256":
            hasher = hashlib.sha256()
        elif chksum == "sha384":
            hasher = hashlib.sha384()
        elif chksum == "sha512":
            hasher = hashlib.sha512()
        else:
            hasher = hashlib.sha256()

        with open( filename, 'rb') as f:
            buf = f.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(BLOCKSIZE)

        self._hash = hasher.hexdigest()
        return hasher.hexdigest()


if __name__ == "__main__":
    pass
