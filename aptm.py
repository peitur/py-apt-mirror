#!/usr/bin/env python3

import os, re, sys

import aptmirror

def print_help( ):
    pass

if __name__ == "__main__":

    if len( sys.argv ) > 1:
        aptmirror.run.Runner( sys.argv )
    else:
        print_help()
