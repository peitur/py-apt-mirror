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


    for comp in components:
        links.append( "%s/%s/binary-%s/Packages.gz" % ( url, comp, arch ) )
        links.append( "%s/%s/binary-%s/Packages.bz2" % ( url, comp, arch ) )
        links.append( "%s/%s/binary-%s/Packages.xz" % ( url, comp, arch ) )

    return links

def generate_package_noncomponent_links( uri, distribution, **opt ):
    links = list()
    links.append( "%s/%s/Packages.gz" % ( uri, distribution ) )
    links.append( "%s/%s/Packages.bz2" % ( uri, distribution ) )
    links.append( "%s/%s/Packages.xz" % ( uri, distribution ) )
    return links.copy()





class MirrorPackages( object ):

    def __init__( self ):
        pass



if __name__ == "__main__":
    pass
