#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.mirror.local
import aptmirror.url

from pprint import pprint

class MirrorTranslateItem( object ):

    def __init__( self, url, path, **opt ):
        self._options = opt
        self._debug = False

        self._url = url
        self._path = path
        self._remote_file = "%s/%s" % ( self._url, self._path )

        self._info = dict()

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def _parse( self ):
        pass

    def download( self, to ):
        try:

            pfields = re.split( r"/+", self._path )
            lfile = pfields.pop(-1)
            lpath = "%s/%s/%s" % ( to, "/".join( pfields ), lfile )
            pathlib.Path( "%s/%s" % (to,  "/".join( pfields ) ) ).mkdir( parents=True, exist_ok=True )
            print( "Download %s to %s" % ( self._remote_file, lpath ) )
            aptmirror.url.download_file( self._remote_file, lpath )

        except Exception as e:
            pprint( e )
            return False
        return True

    def info( self ):
        return self._info.copy()

    def url( self ):
        return self._remote_file



class MirrorTranslateIndex( object ):

    def __init__( self, url, path, **opt ):
        self._options = opt
        self._debug = False

        self._url = url
        self._path = path
        self._index = "i18n/Index"
        self._remote_file = "%s/%s/%s" % ( self._url, self._path, self._index )

        self._info = dict()

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def _parse( self ):
        pass

    def download( self, to ):
        try:

            pfields = re.split( r"/+", self._path )
            lfile = pfields.pop(-1)
            lpath = "%s/%s/%s" % ( to, "/".join( pfields ), lfile )
            pathlib.Path( "%s/%s" % (to,  "/".join( pfields ) ) ).mkdir( parents=True, exist_ok=True )
            print( "Download %s to %s" % ( self._remote_file, lpath ) )
            aptmirror.url.download_file( self._remote_file, lpath )

        except Exception as e:
            pprint( e )
            return False
        return True

    def info( self ):
        return self._info.copy()

    def url( self ):
        return self._remote_file



class MirrorTranslate( object ):

    def __init__( self, uri, distribution, components=list(), **opt ):
        self._options = opt
        self._debug = False

        self._uri = uri
        self._distribution = distribution
        self._components = components

        self._index_files = list()
        self._translate_files = list()

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


    def _index_items( self ):
        pass

    def _translate_index( self ):
        pass

    def download( self, to ):
        pass

    def get( self ):
        pass




if __name__ == "__main__":
    pass
