#!/usr/bin/env python3

import os, re, sys
import tarfile, zipfile, bz2
import random, string
import json

from pprint import pprint

def is_type( o, t ):
    if type( o ).__name__ == t:
        return True
    return False

def temp_dir( root="/tmp", prefix="py" ):
    return "%s/%s_%s" % ( root, prefix, random_string( 6 )  )

def random_string( length ):
    return ''.join(random.SystemRandom().choice( string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range( length ))


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



if __name__ == "__main__":
    pass
