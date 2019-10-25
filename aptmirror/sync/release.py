#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.mirror.local


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

    def _parse( self ):
        pass

    def download( self, to ):
        pass

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

    def _release_items( self ):
        for f in self._files:
            self._items.append( MirrorReleaseItem( self._url, f ) )

        for c in self._components:
            self._items.append( MirrorReleaseItem( self._url, "binary-%s/%s" % (  self._arch, "Release") ))
            self._items.append( MirrorReleaseItem( self._url, "source/%s" % ( "Release" ) ))


    def append_item( self, prefix, fname = "Release" ):
        self._items.append( MirrorReleaseItem( self._url, "%s/%s" % (  prefix, fname ) ) )

    def url( self ):
        return self._url

    def urls( self ):
        return [ i.url() for i in self._items ]

    def download( self, to ):
        return [ i.download( to ) for i in self._items ]


if __name__ == "__main__":
    pass
