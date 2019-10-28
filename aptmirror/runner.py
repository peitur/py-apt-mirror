#!/usr/bin/env python3

import os, re, sys
from pprint import pprint

import aptmirror.sync.config
import aptmirror.sync.lock
import aptmirror.sync.store
import aptmirror.sync.release

"""
    This file defines the external command execution,
    input from user via cli and the actual excution.
    I.e. main tool logic
"""

OPTIONS={}

class MainRunner( object ):

    def __init__( self, args, **opt ):
        self._opt = opt
        self._args = args
        self._debug = False
        self._mirror_config = None
        self._store = None

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


    def run( self ):

        if len( self._args ) == 1:
            raise ArgumentError("Missing configurationh file")

        self._mirror_config = aptmirror.sync.config.MirrorConfig( self._args[1] )

        store = aptmirror.sync.store.LocalMirrorRepo( self._mirror_config.get( "var_path" ) )
        if not store.exists():
            store.create()

        lock = aptmirror.sync.lock.MirrorLock( self._mirror_config.get( "var_path" ) )
        print("# Starting sync of '%s', lockfile: '%s'" % ( self._mirror_config.filename() , lock.lockfile()) )
        if lock.is_locked( ):
            raise OSError("Mirror already locked for other task: %s" % ( lock.lockfile() ) )
        lock.lock()

        try:
            for c in self._mirror_config.get_mirrors():
                arch = c.get_arch()
                uri = c.get_uri()
                suite = c.get_suite()
                comps = c.get_components()

                print("Download to %s" % ( self._mirror_config.get( "mirror_path" ) ) )
                for a in arch:
                    rel = aptmirror.sync.release.MirrorReleases( a, uri, suite, comps, **self._opt )
                    rel.download( self._mirror_config.get( "mirror_path" ) )

        except Exception as e:
            raise e
        finally:
            lock.unlock()

    def get_options( ):
        return "<mirror.list>"

if __name__ == "__main__":
    pass
