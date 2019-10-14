#!/usr/bin/env python3
"""
    Handles local storage
"""

import os, re, sys
import tarfile, zipfile, bz2
import random, string
import json
import pathlib

from pprint import pprint

REPO_FILES=("ALL", "NEW", "MD5", "SHA1", "SHA256")

class LocalRepo( object ):

    def __init__( self, path, **opt ):
        self._debug = False
        self._path = pathlib.Path( path )

        self._options = opt

    def create_structure( self ):
        if not self._path.exists():
            self._path.mkdir( mode=0o755, parents=True )

        for f in REPO_FILES:
            p = pathlib.Path( "%s/%s" % ( self._path, f ) )
            pprint( p )


class LocalStore( object ):

    def __init__( self, path, **opt ):
        pass
