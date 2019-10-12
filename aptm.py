#!/usr/bin/env python3

import os, re, sys

from pprint import pprint

import aptmirror
import aptmirror.runner


def print_help( ):
    pass

if __name__ == "__main__":

    if len( sys.argv ) > 1:
        try:
            aptmirror.runner.MainRunner( sys.argv ).run()
        except Exception as e:
            pprint( e )
    else:
        print_help()
