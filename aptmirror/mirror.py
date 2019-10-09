#!/usr/bin/env python3

import os, re, sys
import pathlib

import aptmirror.validate
import aptmirror.utils

from pprint import pprint

"""
    This file contains everything for the mirror file/config handling
"""

DEFAULT_CONFIG={
    "nthreads": 20,
    "limit_rate": '100m',
    "base_path": '/var/spool/apt-mirror',
    "mirror_path": '$base_path/mirror',
    "skel_path": '$base_path/skel',
    "var_path": '$base_path/var',
    "cleanscript": '$var_path/clean.sh',
    "run_postmirror": 1,
    "auth_no_challenge": 0,
    "no_check_certificate": 0,
    "unlink": 0,
    "postmirror_script": '$var_path/postmirror.sh',
    "use_proxy": 'off',
    "http_proxy": '',
    "https_proxy": '',
    "proxy_user": '',
    "proxy_password": ''
}

class MirrorConfig( object ):

    def __init__( self, filename, **opt ):
        self._config = DEFAULT_CONFIG
        self._mirrors = list()
        self._filename = filename
        self._debug = False
        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

        cf = pathlib.Path( self._filename )
        if not cf.exists():
            raise OSError("No such file %s" % ( self._filename ) )

        self._apply_variables()

    def _parse( self ):
        pass

    def _apply_variables( self ):
        for k1 in self._config:
            k = "$%s" % ( k1 )
            for k2 in self._config:
                if aptmirror.utils.is_type( self._config[k1], "str" ) and aptmirror.utils.is_type( self._config[k2], "str" ):
                    self._config[k2] = re.sub( re.escape(k), self._config[k1], self._config[k2] )

    def get_config( self ):
        return self._config

if __name__ == "__main__":
    m = MirrorConfig( "mirror.py" )
    pprint( m.get_config() )
