#!/usr/bin/env python3

import os, re, sys
from pprint import pprint

import aptmirror.mirror.config
import aptmirror.mirror.store
import aptmirror.mirror.local

"""
    This file defines the external command execution,
    input from user via cli and the actual excution.
    I.e. main tool logic
"""

OPTIONS={}

class MainRunner( object ):

    def __init__( self, args, **opt ):
        self._args = args
        self._debug = False
        self._mirror_config = None
        self._store = None

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


    def run( self ):

        if len( self._args ) > 1:
            self._mirror_config = aptmirror.mirror.config.MirrorConfig( self._args[1] )
            pprint( self._mirror_config.get_config() )

            for mi in self._mirror_config.get_mirrors():
                pprint( mi.get_index_links() )
            self._store = aptmirror.mirror.store.LocalMirrorRepo( self._mirror_config.get( "var_path" ) )
            self._store.create_structure()

        else:
            raise AttributeError("No input file")

    def get_options( ):
        return "<mirror.list>"

if __name__ == "__main__":
    pass
