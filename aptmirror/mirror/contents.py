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

def generate_package_component_links( arch, uri, distribution, components=list(), **opt ):
    links = list()
    contents = False

    if 'contents' in opt and opt['contents'] in (True, False):
        contents = opt['contents']

    url = "%s/dists/%s" % ( uri, distribution )

    if contents:
        links.append( "%s/Contents-%s.gz" % ( url, arch ) )
        links.append( "%s/Contents-%s.bz2" % ( url, arch ) )
        links.append( "%s/Contents-%s.xz" % ( url, arch ) )

        if contents:
            links.append( "%s/%s/Contents-%s.gz" % ( url, comp, arch ) )
            links.append( "%s/%s/Contents-%s.bz2" % ( url, comp, arch ) )
            links.append( "%s/%s/Contents-%s.xz" % ( url, comp, arch ) )

    return links

class MirrorPackageContents( object ):

    def __init__( self ):
        pass
