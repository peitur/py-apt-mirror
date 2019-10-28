#!/usr/bin/env python3

import os, re, sys
import requests
import pathlib

def download_file_wget( source, target, **options ):
    pass

def download_file_0( url_filename, local_filename, proxy={}, **opt ):

    x_size = 0
    l_size = 0
    r_size = 0
    bsize=1024
    overwrite = False
    timeout = 10
    debug = False
    check_certificate = True

    proxies = urllib.request.getproxies()

    if 'debug' in opt: debug = opt['debug']
    if 'bsize' in opt: bsize = opt['bsize']
    if 'timeout' in opt: timeout = opt['timeout']

    if 'overwrite' in opt and opt['overwrite'] in (True,False):
        overwrite = opt['overwrite']

    if 'check_certificate' in opt and opt['no_check_certificate'] in (True, False):
        check_certificate = not opt['no_check_certificate']

    if pathlib.Path( local_filename ).exists():
        l_size = pathlib.Path( local_filename ).stat().st_size

    r = requests.get( url_filename, timeout=timeout, stream=True, proxies=proxies, verify=check_certificate )
    if 'content-length' in r.headers:
        r_size = r.headers['content-length']

    if debug:
        pprint( r.headers )

    if r.status_code != 200:
        print("# ERROR: Could not find %s,  %s : " % ( url_filename, r.status_code ) )
        return None

    if not pathlib.Path( local_filename ).exists() or overwrite:
        with open( local_filename, 'wb') as f:
            for chunk in r.iter_content( chunk_size=bsize ):
                if chunk: # filter out keep-alive new chunks
                    x_size += len( chunk )
                    f.write(chunk)
    r.close()

    return local_filename

def download_file( url_filename, local_filename, **opt ):
    x_size = 0
    l_size = 0
    r_size = 0
    bsize=1024
    overwrite = False
    timeout = 10
    debug = False

    if 'debug' in opt: debug = opt['debug']
    if 'bsize' in opt: bsize = opt['bsize']
    if 'timeout' in opt: timeout = opt['timeout']

    if 'overwrite' in opt and opt['overwrite'] in (True,False):
        overwrite = opt['overwrite']

    if pathlib.Path( local_filename ).exists():
        l_size = pathlib.Path( local_filename ).stat().st_size

    r = requests.get( url_filename, timeout=timeout, stream=True)
    if 'content-length' in r.headers:
        r_size = r.headers['content-length']

    if debug:
        pprint( r.headers )

    if r.status_code != 200:
        print("# ERROR: Could not find %s,  %s : " % ( url_filename, r.status_code ) )
        return None

    if not pathlib.Path( local_filename ).exists() or overwrite:
        with open( local_filename, 'wb') as f:
            for chunk in r.iter_content( chunk_size=bsize ):
                if chunk: # filter out keep-alive new chunks
                    x_size += len( chunk )
                    f.write(chunk)

    r.close()

    return local_filename
