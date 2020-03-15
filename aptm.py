#!/usr/bin/env python3

import os, re, sys

from pprint import pprint

import aptmirror
import aptmirror.frmt as frmt
import aptmirror.runner


def print_help( ):
    pass

if __name__ == "__main__":

    if len( sys.argv ) > 1:
        try:
            aptmirror.runner.MainRunner( sys.argv ).run()
        except Exception as e:
            print("ERROR: %s%s%s" % ( frmt.Quick.fail(), e, frmt.Quick.nc() ))
            raise e
    else:
        print_help()
