# subnet-hosts.py
# Preforms an ICMP sweep over all the ips
# of a subnet to find all active hosts

# Author: Fred Song, xx@uvic.ca

import sys
import os

import threading

class IPNetwork():
    def __init__(self, net_prefix, prefix_length):
        # ex. ip = "192.168.20.200"

        self.prefix_length = int(prefix_length)
        bin_ip = IPNetwork.str_to_bin(net_prefix)
        for i in xrange(0,32): 
            bin_ip[i] = bin_ip[i] if i<self.prefix_length else "0";

        self.net_prefix = bin_ip

    @staticmethod 
    def str_to_bin(ip):
        arr = ip.split(".")
        bin_ip = []

        for a in arr:
            # ex. a = "192"
            part = bin(int(a)) #0b1100100
            part = list(part.split("b")[1])
            part = ["0"]*(8-len(part)) + part
            bin_ip += part

        assert len(bin_ip) == 32
        return bin_ip

    @staticmethod
    def bin_to_str(ip):
        assert len(ip) == 32

        p1 = "".join(ip[0:8])
        p2 = "".join(ip[8:16])
        p3 = "".join(ip[16:24])
        p4 = "".join(ip[24:32])

        return "%s.%s.%s.%s" % (int(p1,2), int(p2,2), int(p3,2), int(p4,2))

    def __str__(self):
        return "%s/%s" % (IPNetwork.bin_to_str(self.net_prefix), self.prefix_length)

    def get_network_ips(self):
        min_ip = int("".join(self.net_prefix), 2) 

        max_ip_bin = self.net_prefix[0:self.prefix_length] + ["1"]*(32-self.prefix_length)
        max_ip = int("".join(max_ip_bin), 2)

        ips = []
        for int_ip in xrange(min_ip+1, max_ip):
            bin_ip =  bin(int_ip).split('b')[1]
            bin_ip = ["0"]*(32-len(bin_ip)) + list(bin_ip)
            ips.append(IPNetwork.bin_to_str(bin_ip))

        return ips

class CheckIPThread(threading.Thread):
    def __init__(self, ip, callback):
        threading.Thread.__init__(self)
        self.ip = ip
        self.callback = callback

    def run(self):
        exists = CheckIPThread.ping(self.ip)
        self.callback(self.ip,exists)

    @staticmethod
    def ping(ip, deadline=1):
        return (os.system("ping -w%s %s > /dev/null" % (deadline,ip)) == 0)

def test():
    print IPNetwork("192.168.20.200","24").get_network_ips()
    print "---"
    print IPNetwork("10.175.132.0","24").get_network_ips()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "usage: %s <network_prefix>/<prefix_length>" % sys.argv[0]
        exit(1)
    
    if sys.argv[1] == "TEST":
        test()
        exit(0)

    network_info = sys.argv[1].split('/')
    net_prefix = network_info[0]
    prefix_length = network_info[1]

    net = IPNetwork(net_prefix, prefix_length)


    def print_ip(ip, exists):
        if exists:
            print ip
    for ip in net.get_network_ips():
        CheckIPThread(ip, print_ip).start()

    exit(0)
