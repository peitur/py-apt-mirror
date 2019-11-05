#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.mirror.local


from pprint import pprint

class MirrorTranslateItem( object ):

    def __init__( self, url, path, **opt ):
        self._options = opt
        self._debug = False

        self._url = url
        self._path = path
        self._remote_file = "%s/%s" % ( self._url, self._path )

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def download( self ):
        pass


class MirrorTranslateIndex( object ):

    def __init__( self, url, path, **opt ):
        self._options = opt
        self._debug = False

        self._url = url
        self._path = path
        self._index = "i18n/Index"
        self._remote_file = "%s/%s/%s" % ( self._url, self._path, self._index )

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def download( self ):
        pass



class MirrorTranslate( object ):

    def __init__( self, uri, distribution, components=list(), **opt ):
        self._options = opt
        self._debug = False

        self._uri = uri
        self._distribution = distribution
        self._components = components



        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']




if __name__ == "__main__":
    pass
