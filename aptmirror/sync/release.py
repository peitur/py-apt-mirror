#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.local
import aptmirror.url

from pprint import pprint

class MirrorReleaseItem( object ):

    def __init__(self, url, path, **opt ):
        self._options = opt
        self._debug = False

        self._url = url
        self._path = path
        self._remote_file = "%s/%s" % ( self._url, self._path )

        self._info = dict()

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


    def _parse( self, fname = None ):
        if not fname:
            fname = self._path

        data = aptmirror.local.load_file( fname )
        for d in data:
            flds = [ x.lstrip().rstrip() for x in re.split( r"\:", d ) ]
            self._info[ flds[0].lower() ] = flds[1].lower()

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

    def info( self ):
        return self._info.copy()

    def get( self, k ):
        if not self._info:
            raise RuntimeError( "Release info missing" )

        if k not in self._info:
            raise AttributeError("Missing key %s in release info" % ( k ) )

        return self._info[k]

    def url( self ):
        return self._remote_file

class MirrorReleases( object ):

    def __init__(self, arch, uri, distribution, components=list(), **opt ):
        self._options = opt
        self._debug = False

        self._arch = arch
        self._uri = uri
        self._distribution = distribution
        self._components = components

        self._files = ["Release", "InRelease"]
        self._signatrue = "Release.gpg"
        self._url = "%s/dists/%s" % ( self._uri, self._distribution )
        self._files = ["InRelease", "Release", "Release.gpg"]

        self._items = list()

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

        self._release_items()

    def _release_items( self ):
        for f in self._files:
            self._items.append( MirrorReleaseItem( self._url, f ) )

        for c in self._components:
            self._items.append( MirrorReleaseItem( self._url, "%s/binary-%s/%s" % (  c, self._arch, "Release") ))
            self._items.append( MirrorReleaseItem( self._url, "%s/source/%s" % ( c, "Release" ) ))

    def url( self ):
        return self._url

    def urls( self ):
        return [ i.url() for i in self._items ]

    def download( self, to ):
        return [ i.download( to ) for i in self._items ]


if __name__ == "__main__":
    pass
