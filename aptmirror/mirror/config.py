#!/usr/bin/env python3

import os, re, sys
import pathlib
import json

import aptmirror.validate
import aptmirror.utils
import aptmirror.command

import aptmirror.mirror.local

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
    "run_postmirror": True,
    "auth_no_challenge": False,
    "no_check_certificate": False,
    "unlink": False,
    "postmirror_script": '$var_path/postmirror.sh',
    "use_proxy": False,
    "http_proxy": None,
    "https_proxy": None,
    "proxy_user": None,
    "proxy_password": None
}

DEFAULT_ARCH="amd64"

def generate_src_component_links( uri, distribution, components=list(), **opt ):
    links = list()

    url = "%s/dists/%s" % ( uri, distribution )

    links.append( "%s/InRelease" % ( url ) )
    links.append( "%s/Release" % ( url ) )
    links.append( "%s/Release.gpg" % ( url ) )

    for comp in components:
        links.append( "%s/%s/source/Release" % ( url, comp ) )
        links.append( "%s/%s/source/Sources.gz" % ( url, comp ) )
        links.append( "%s/%s/source/Sources.bz2" % ( url, comp ) )
        links.append( "%s/%s/source/Sources.xz" % ( url, comp ) )

    return links.copy()


def generate_src_noncomponent_links( uri, distribution, **opt ):
    links = list()
    links.append( "%s/%s/Release" % ( uri, distribution ) )
    links.append( "%s/%s/Release.gpg" % ( uri, distribution ) )
    links.append( "%s/%s/Sources.gz" % ( uri, distribution ) )
    links.append( "%s/%s/Sources.bz2" % ( uri, distribution ) )
    links.append( "%s/%s/Sources.xz" % ( uri, distribution ) )
    return links.copy()


def generate_binary_component_links( arch, uri, distribution, components=list(), **opt ):
    links = list()
    contents = False

    if 'contents' in opt and opt['contents'] in (True, False):
        contents = opt['contents']

    url = "%s/dists/%s" % ( uri, distribution )

    links.append( "%s/InRelease" % ( url ) )
    links.append( "%s/Release" % ( url ) )
    links.append( "%s/Release.gpg" % ( url ) )

    if contents:
        links.append( "%s/Contents-%s.gz" % ( url, arch ) )
        links.append( "%s/Contents-%s.bz2" % ( url, arch ) )
        links.append( "%s/Contents-%s.xz" % ( url, arch ) )

    for comp in components:
        links.append( "%s/%s/binary-%s/Release" % ( url, comp, arch ) )
        links.append( "%s/%s/binary-%s/Packages.gz" % ( url, comp, arch ) )
        links.append( "%s/%s/binary-%s/Packages.bz2" % ( url, comp, arch ) )
        links.append( "%s/%s/binary-%s/Packages.xz" % ( url, comp, arch ) )
        links.append( "%s/%s/i18n/Index" % ( url, comp ) )

        if contents:
            links.append( "%s/%s/Contents-%s.gz" % ( url, comp, arch ) )
            links.append( "%s/%s/Contents-%s.bz2" % ( url, comp, arch ) )
            links.append( "%s/%s/Contents-%s.xz" % ( url, comp, arch ) )

    return links

def generate_binary_noncomponent_links( uri, distribution, **opt ):
    links = list()
    links.append( "%s/%s/Release" % ( uri, distribution ) )
    links.append( "%s/%s/Release.gpg" % ( uri, distribution ) )
    links.append( "%s/%s/Packages.gz" % ( uri, distribution ) )
    links.append( "%s/%s/Packages.bz2" % ( uri, distribution ) )
    links.append( "%s/%s/Packages.xz" % ( uri, distribution ) )
    return links.copy()





class MirrorCleanItem( object ):
    def __init__( self, line, **opt ):
        self._line = line.lstrip().rstrip()
        self._debug = False

        self._clean = False
        self._uri = None

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

        self._parse()

    def __str__( self ):
        return json.dumps( self.__dict__() )

    def __dict__( self ):
        return { "clean": self._clean, "uri": self._uri }

    def _fields( self ):
        return [ x.rstrip().lstrip() for x in re.split( r"\s+", self._line ) ]

    def _parse( self ):

        fields = self._fields()

        if fields[0] == "clean":
            self._clean = True
            self._uri = fields[1]

        elif fields[0] == "clean":
            self._clean = False
            if len( fields ) > 1:
                self._uri = fields[1]
        else:
            raise RuntimeError( "Bad cleanup reference" )

        return self.__dict__()

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

        self._type = "binary"
        self._arch = list()
        self._uri = None
        self._options = dict()
        self._suite = None
        self._components = list()

        self._contents = True

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

        if 'contents' in opt and opt['contents'] in (True, False):
            self._contents = opt['contents']

        self._parse_mirror()

    def __str__( self ):
        return json.dumps( self.__dict__() )

    def __dict__( self ):
        return { "type": self._type, "arch": self._arch.copy(), "options": self._options.copy(), "uri": self._uri, "suite": self._suite, "components": self._components.copy() }

    def _fields( self ):
        return [ x.rstrip().lstrip() for x in re.split( r"\s+", self._line ) ]


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
        fields = [ x.rstrip().lstrip() for x in re.split( r"\s+", self._line ) ]

        if re.match( r"deb-src", fields[0] ):
            self._type = "source"

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

        return self.__dict__()

    def get_index_links( self ):
        links = dict()
        data = self._parse_mirror()

        if self._type == "binary":
            for a in self._arch:

                if len( self._components ) > 0:
                    urls = generate_binary_component_links( a, self._uri, self._suite, self._components )
                    for url in urls:
                        links[ url ] = dict()
                else:
                    urls = generate_binary_noncomponent_links( a, self._uri, self._suite )
                    for url in urls:
                        links[ url ] = dict()


        elif self._type == "source":
            if len( self._components ) > 0:
                urls = generate_src_component_links( self._uri, self._suite, self._components )
                for url in urls:
                    links[ url ] = dict()

            else:
                urls = generate_src_noncomponent_links( self._uri, self._suite )
                for url in urls:
                    links[ url ] = dict()

        else:
            raise AttributeError("No such type %s" % (self._type ) )

        return links



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

    def get_type( self ):
        return self._type

    def get_fields( self ):
        return self._fields()

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
            if aptmirror.utils.is_type( self._config[ fields[1] ], "boolean" ):
                if int( fields[2] ) == 0:
                    self._config[ fields[1] ] = False
                elif int( fields[2] ) == 1:
                    self._config[ fields[1] ] = True
            else:
                self._config[ fields[1] ] = fields[2]


    def _parse( self ):
        data = aptmirror.mirror.local.load_file( self._filename )
        for line in data:
            if len( line ) > 0:
                fields = [ x.rstrip().lstrip() for x in re.split( r"\s+", line ) ]
                if re.match( r"\s*set", fields[0] ):
                    self._parse_set( fields )
                elif re.match( r"\s*deb.*", fields[0] ):
                    m = MirrorItem( line, debug=self._debug )
                    self._mirrors.append( m )
                elif re.match( r"\s*(clean|skip-clean).*", fields[0] ):
                    m = MirrorCleanItem( line, debug=self._debug )
                    self._cleanups.append( m )


    def _apply_variables( self ):
        for k1 in self._config:
            k = "$%s" % ( k1 )
            for k2 in self._config:
                if aptmirror.utils.is_type( self._config[k1], "str" ) and aptmirror.utils.is_type( self._config[k2], "str" ):
                    self._config[k2] = re.sub( re.escape(k), self._config[k1], self._config[k2] )

    def get_config( self ):
        return self._config.copy()

    def get( self, key ):
        if key not in self._config:
            raise AttributeError("No such configuration key %s" % ( key ) )
        return self._config[ key ]


    def get_mirrors( self ):
        return self._mirrors.copy()

    def run_postmirror( self ):
        pass

if __name__ == "__main__":
    m = MirrorConfig( "../test/mirror.list" )
    pprint( m.get_mirrors() )
