#!/usr/bin/env python3

import os, re, sys
import tarfile, zipfile, bz2
import random, string
import json
import pathlib

from pprint import pprint

def is_type( o, t ):
    if type( o ).__name__ == t:
        return True
    return False

def random_string( length ):
    return ''.join(random.SystemRandom().choice( string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range( length ))


if __name__ == "__main__":
    pass
