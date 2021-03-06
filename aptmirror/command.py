#!/usr/bin/env python3

"""
    This file defines the CLI behaviour
"""

import os, sys, re
import subprocess, shlex

from pprint import pprint

def run( cmd, **opt ):
        result = list()
        debug = False
        if 'debug' in opt and opt['debug'] in (True, False):
            debug = opt['debug']

        if type( cmd ).__name__ == "str":
            cmd = shlex.split( cmd )

        if debug: print( "Running: '%s'" % ( " ".join( cmd ) ) )

        prc = subprocess.Popen( cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True )
        for line in prc.stdout.readlines():
            result.append( line )
            if prc.poll():
                break

        return (prc.returncode, result)



def run_iter( cmd, **opt ):
        debug = False
        if 'debug' in opt and opt['debug'] in (True, False):
            debug = opt['debug']

        if type( cmd ).__name__ == "str":
            cmd = shlex.split( cmd )

        if debug: print( "Running: '%s'" % ( " ".join( cmd ) ) )

        prc = subprocess.Popen( cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True )
        for line in prc.stdout.readlines():
            yield line.rstrip()

            if prc.poll():
                break




if __name__ == "__main__":
    pass
