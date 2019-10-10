#!/usr/bin/env python3

import os, re, sys
import pathlib

import aptmirror.validate
import aptmirror.utils
import aptmirror.command

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
    "use_proxy": False,
    "http_proxy": None,
    "https_proxy": None,
    "proxy_user": None,
    "proxy_password": None
}

DEFAULT_ARCH="amd64"

class MirrorCleanItem( object ):
    def __init__( self, line, **opt ):
        self._line = line.lstrip().rstrip()
        self._debug = False

        self._clean = False
        self._uri = None

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

    def _parse( self ):

        fields = re.split( r"\s+", self._line )
        if fields[0] == "clean":
            self._clean = True
            self._uri = fields[1]

        elif fields[0] == "clean":
            self._clean = False
            if len( fields ) > 1:
                self._uri = fields[1]
        else:
            raise RuntimeError( "Bad cleanup reference" )

        return { "clean": self._clean, "uri": self._uri }

    def parse( self ):
        return self._parse()

    def get_clean( self ):
        return self._clean

    def get_uri( self ):
        return self._uri


class MirrorItem( object ):

    def __init__( self, line, **opt ):
        self._line = line.lstrip().rstrip()
        self._debug = False

        self._arch = list()
        self._uri = None
        self._options = dict()
        self._suite = None
        self._components = list()

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']


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
        return data.copy()


    def _parse_mirror( self ):
        fields = re.split( r"\s+", self._line )

        m = re.match( r".*\[(.+)\].*", self._line )
        if m:
             self._options = self._parse_options( m.group(1).lstrip().rstrip() )
             fields = re.split( r"\s+", re.sub( r"\[(.+)\]", "", self._line ) )

        self._arch = [ self._parse_mirror_arch( fields.pop(0) ) ]
        if len( self._options ) > 0:
            self._arch = self._options['arch']

        self._uri = fields.pop(0)
        self._suite = fields.pop(0)
        self._components = fields.copy()

        return { "arch": self._arch.copy(), "options": self._options.copy(), "uri": self._uri, "suite": self._suite, "components": self._components.copy() }

    def get_arch( self ):
        return self._arch.copy()

    def get_suite( self ):
        return self._suite

    def get_uri( self ):
        return self._uri

    def get_components( self ):
        return self._components.copy()

    def get_options( self ):
        return self._options.copy()

    def parse( self ):
        return self._parse_mirror()




class MirrorConfig( object ):

    def __init__( self, filename, **opt ):
        self._config = DEFAULT_CONFIG.copy()
        self._mirrors = list()
        self._cleanups = list()

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


    def _parse( self ):
        data = aptmirror.utils.load_file( self._filename )
        for line in data:
            if len( line ) > 0:
                fields = re.split( "\s+", line )
                if re.match( r"\s*set", fields[0] ):
                    self._parse_set( fields )
                elif re.match( r"\s*deb.*", fields[0] ):
                    self._mirrors.append( MirrorItem( line, debug=self._debug ).parse() )
                elif re.match( r"\s*(clean|skip-clean).*", fields[0] ):
                    self._cleanups.append( MirrorCleanItem( line, debug=self._debug ).parse() )


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

    def run_postmirror( self ):
        pass

if __name__ == "__main__":
    m = MirrorConfig( "../test/mirror.list" )
    pprint( m.get_mirrors() )
