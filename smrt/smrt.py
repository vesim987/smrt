#!/usr/bin/env python

import socket, time, random, argparse, logging

from .protocol import *
from .network import SwitchConversation
from .operations import *

def loglevel(x):
    try:
        return getattr(logging, x.upper())
    except AttributeError:
        raise argparse.ArgumentError('Select a proper loglevel')

def main():
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument('--configfile', '-c')
    parser.add_argument('--switch-mac', '-s')
    parser.add_argument('--host-mac', )
    parser.add_argument('--ip-address', '-i')
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    parser.add_argument('--loglevel', '-l', type=loglevel, default='INFO')
    parser.add_argument('action')
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    switch_mac = args.switch_mac
    host_mac = args.host_mac
    ip_address = args.ip_address

    sc = SwitchConversation(switch_mac, host_mac, ip_address)

    sc.login(args.username, args.password)

    if args.action == 'query_port_mirror':
        header, payload = sc.query(GET, query_port_mirror_payload())
        print(payload)
    elif args.action == 'status':
        header, payload = sc.query(GET, query_port_8021q_vlan_status())
        for id, data in payload:
            if id != 8705:
                continue
            # print(repr(data))
            id_, untagged, tagged = struct.unpack("!HII", data[0:10])
            name = data[10:].rstrip(b'\0').decode()
            print(name)
            for i in range(8):
                print(f"{i} : {'tagged' if (tagged >> i & 1) else 'untagged' if (untagged >> i & 1) else 'disabled'} ")

if __name__ == "__main__":
    main()
