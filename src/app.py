#!/usr/bin/python

import miniupnpc

import logging
import configobj
import platform

from configobj import ConfigObj

# miniupnpc example (and only doc here):
# https://github.com/miniupnp/miniupnp/blob/master/miniupnpc/testupnpigd.py



CONFIG = '/home/jkx/igd-mapper.ini'
PKG_NAME = 'igd-mapper'

upnp = None
cfg = None

logger = logging.getLogger(PKG_NAME)

def setup():
    global upnp
    #coloredlogs.install(level='DEBUG')
    #logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
    logger.debug('UPnP discovery')
    upnp = miniupnpc.UPnP()
    upnp.discover()
    try:
        logger.debug('Found IGD: ' + upnp.selectigd())
    except Exception:
        logger.warning('Unable to find internet gateway')
        upnp = None

def bytes_to_string(value):
    return '%sMB' % int(value/1024/1024)


def load_cfg(filename):
    global cfg
    cfg = ConfigObj(filename,indent_type='  ',encoding="utf8")


def get_sig():
    return '%s-%s' % (PKG_NAME,platform.node())

def cleanup():
    i = 0
    to_delete = []

    while True:
        r = upnp.getgenericportmapping(i)
        if r == None:
            break
        if r[3].startswith(get_sig()):
            to_delete.append((r[0],r[1]))
        i = i+1
    #
    for m in to_delete:
        upnp.deleteportmapping(m[0],m[1])

def mapp():
    rules = cfg.get('rules',[])
    for r in rules:
        external = rules[r].get('external',None)
        internal = rules[r].get('internal',None)
        proto = rules[r].get('proto',None)
        ip = rules[r].get('ip',None)

        if external == None:
            logger.error(f"wrong external port for {r}")
            break
        if internal == None: 
            internal = external
        if proto == None:
            proto = 'TCP'
        if ip == None:
            ip = upnp.lanaddr

        external = int(external)
        internal = int(internal)
        try:
            upnp.addportmapping(external, proto,ip, internal, '%s:%s'% (get_sig(),r), '')
        except Exception as e:
            pass


def show_info():
    print("Network config")
    print("==============")
    print(f"Connexion: \t" + upnp.connectiontype() )
    print(f"External IP:\t" + upnp.externalipaddress() ) 
    print(f"Local IP:\t" + upnp.lanaddr )
    print("Stats:   \t%s sent / %s recv " % (bytes_to_string(upnp.totalbytesent()) ,bytes_to_string(upnp.totalbytereceived())))
    print()

def show_mapping():
    print("UPnP Rules")
    print("==========")
    i = 0
    while True:
        r = upnp.getgenericportmapping(i)
        
        if r == None:
            break
        #print(r)
        print(f"{r[3]}\t{r[1]} {r[0]}\t=> {r[2]}")
        i = i+1
    print()

def main():
    load_cfg(CONFIG)
    show_info()
    #show_mapping()
    cleanup()
    mapp()
    show_mapping()


if __name__ == '__main__':
    setup()
    if upnp:
        main()