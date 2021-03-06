#!/usr/bin/env python3
"""
    Handles lcoal util file operations operations
"""

import os, re, sys
import tarfile, zipfile, bz2
import random, string
import json
import pathlib


def dir_tree( path, rx=r".*", **opt ):
    res = list()

    p = pathlib.Path( path )
    for c in p.iterdir():
        if c.is_dir():
            res += list( dir_tree( "%s/%s" % ( p, c.name ), rx, **opt ) )
        else:
            if re.match( rx, c.name ):
                res.append( "%s/%s" % ( p, c.name ) )

    return res



def unpack_gz( filename,  ):
    tar = tarfile.open( filename, "r:gz")
    for tarinfo in tar:
        if tarinfo.isreg():
            print("%s a regular file." % (tarinfo) )
        elif tarinfo.isdir():
            print("%s a directory." % (tarinfo) )
        else:
            print("%s something else." % (tarinfo) )
    tar.close()

def _read_text( filename ):
    result = list()
    try:
        fd = open( filename, "r" )
        for line in fd.readlines():
            if not re.match(r"\s*#.*", line ):
                result.append( line.lstrip().rstrip() )
        return result
    except Exception as e:
        print("ERROR Reading %s: %s" % ( filename, e ))

    return result

def _read_json( filename ):
    return json.load( filename )

def load_file( filename ):
    filesplit = re.split( r"\.", filename )
    if filesplit[-1] in ( "json" ):
        return _read_json( filename )
    else:
        return _read_text( filename )

def _write_json( filename, data ):
    return _write_text( filename, json.dumps( data, indent=2, sort_keys=True ) )

def _write_text( filename, data ):
    fd = open( filename, "w" )
    fd.write( str( data ) )
    fd.close()

def write_file( filename, data ):
    filesplit = re.split( "\.", filename )
    if filesplit[-1] in ( "json" ):
        return _write_json( filename, data )
    else:
        return _write_text( filename, data )

def temp_dir( root="/tmp", prefix="py" ):
    return "%s/%s_%s" % ( root, prefix, random_string( 6 )  )


if __name__ == "__main__":
    pprint( dir_tree( ".." ) )
    pprint( dir_tree( "..", r".*\.py$" ) )
