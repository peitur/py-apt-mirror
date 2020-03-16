#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.mirror.local


from pprint import pprint

class Stat( object ):

    def __init__(self ):
        self._options = opt
        self._debug = False
        self._data = list()

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def clear( self ):
        self._data = list()
    
    def register( self, filename ):
        self._data[ filename ] = os.stat( filename )

    def get( self, filename ):
        if filename not in self._data:
            self.add( filename )
        return self._data[ filename ].copy()

    def is_dirty( self, filename, extinfo ):
        fst = self.get( filename )
        

if __name__ == "__main__":
    pass
