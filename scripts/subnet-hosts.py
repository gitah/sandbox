# subnet-hosts.py, Fred Song
# pings and lists all hosts in a subnet

import sys
import os

def ip_up(ip, deadline=1):
    return (os.system("ping -w%s %s > /dev/null" % (deadline,ip)) == 0)

def ips_in_network(net_prefix, prefix_len):
    #TODO: this is the hard part
    pass

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print "usage: %s <network_prefix>/<prefix_length>" % sys.argv[0]
        exit(1)

    network = sys.argv[1].split('/')
    net_prefix = network[0]
    prefix_len = network[1]

    print "Active ips:"
    for ip in ips_in_network(net_prefix, prefix_len):
        if ip_up(ip):
            print ip
    exit(0)
