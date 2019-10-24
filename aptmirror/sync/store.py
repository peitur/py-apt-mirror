#!/usr/bin/env python3
"""
    Handles local storage
"""

import os, re, sys
import tarfile, zipfile, bz2
import random, string
import json
import pathlib

import aptmirror.local

from pprint import pprint

REGISTRY_FILES=("ALL", "NEW", "MD5", "SHA1", "SHA256")

class LocalMirrorRegistry( object ):

    def __init__( self, path, checksum="sha256", **opt ):
        self._debug = False
        self._path = pathlib.Path( path )
        self._checksum = checksum
        self._options = opt
        self._data_q = dict()

        for i in REGISTRY_FILES:
            self._data_q[ i ] = dict()

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


    def create_structure( self ):
        if not self._path.exists():
            self._path.mkdir( mode=0o755, parents=True )

        for f in REGISTRY_FILES:
            p = pathlib.Path( "%s/%s" % ( self._path, f ) )
            if not p.exists():
                p.touch()

    def verify_registry( self ):
        pass

    def load_registry( self, reg ):
        self._data_q["ALL"] = aptmirror.local.load_file( "%s/%s" % ( self._path, "ALL") )
        self._data_q["NEW"] = aptmirror.local.load_file( "%s/%s" % ( self._path, "NEW") )
        self._data_q["MD5"] = aptmirror.local.load_file( "%s/%s" % ( self._path, "MD5") )
        self._data_q["SHA1"] = aptmirror.local.load_file( "%s/%s" % ( self._path, "SHA1") )
        self._data_q["SHA256"] = aptmirror.local.load_file( "%s/%s" % ( self._path, "SHA256") )



class LocalMirrorRepo( object ):

    def __init__( self, path, **opt ):
        self._debug = False
        self._path = pathlib.Path( path )
        self._options = opt

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def exists( self ):
        return self._path.exists()

    def create( self ):
        if not self.exists():
            self._path.mkdir( parents=True )

    def path( self ):
        return self._path


if __name__ == "__main__":
    pass
