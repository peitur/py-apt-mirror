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

DEFAULT_ARCH="amd64"

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

        self._parse()
        self._apply_variables()

    def _parse_set( self, fields ):
        if fields[1] in self._config and len( fields ) == 3:
            if aptmirror.utils.is_type( self._config[ fields[1] ], "int" ):
                self._config[ fields[1] ] = int( fields[2] )
            else:
                self._config[ fields[1] ] = fields[2]

    def _parse_mirror_arch( self, t ):
        if re.match( r"\s*deb$", t ):
            return DEFAULT_ARCH
        else:
            m = re.match( r"\s*deb-(\w+)$", t )
            return m.group(1)

    def _parse_options( self, o ):
        data = dict()
        opts = re.split( r"\s+", o )
        for x in opts:
            d = re.split( r"=", x )
            if re.search( r",", d[1] ):
                data[ d[0] ] = re.split( ",", d[1] )
            else:
                data[ d[0] ] = d[1]
        return data


    def _parse_mirror( self, fields ):
        data = dict()

        data["options"] = None
        m = re.match( r".*\[(.+)\].*", " ".join( fields ) )
        if m:
             data["options"] = self._parse_options( m.group(1).lstrip().rstrip() )
             fields = re.split( r"\s+", re.sub( r"\[(.+)\]", "", " ".join( fields ) ) )
        
        data["arch"] = self._parse_mirror_arch( fields.pop(0) )
        data["url"] = fields.pop(0)
        data["suite"] = fields.pop(0)
        data["components"] = fields.copy()

        return data

    def _parse_clear( self, fields ):
        pass

    def _parse( self ):
        data = aptmirror.utils.load_file( self._filename )
        for line in data:
            if len( line ) > 0:
                fields = re.split( "\s+", line )
                if re.match( r"\s*set", fields[0] ):
                    self._parse_set( fields )
                elif re.match( r"\s*deb.*", fields[0] ):
                    self._mirrors.append( self._parse_mirror( fields ) )


    def _apply_variables( self ):
        for k1 in self._config:
            k = "$%s" % ( k1 )
            for k2 in self._config:
                if aptmirror.utils.is_type( self._config[k1], "str" ) and aptmirror.utils.is_type( self._config[k2], "str" ):
                    self._config[k2] = re.sub( re.escape(k), self._config[k1], self._config[k2] )

    def get_config( self ):
        return self._config.copy()

    def get_mirrors( self ):
        return self._mirrors.copy()

if __name__ == "__main__":
    m = MirrorConfig( "../test/mirror.list" )
    pprint( m.get_mirrors() )
