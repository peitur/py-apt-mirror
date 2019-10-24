#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.mirror.local


from pprint import pprint

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

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


    def url( self ):
        return self._url

if __name__ == "__main__":
    pass
