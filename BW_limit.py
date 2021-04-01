#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getNetworkStatus.py
User:               Guodong
Create Date:        2016/11/2
Create Time:        16:20
Modify by:          HuangBin

show Windows or Linux network Nic status, such as MAC address, Gateway, IP address, etc
and to set the Nic BandWidth, such as:
"sudo python3 BW_limit.py -b 60 -f build"  (to limit 60 Mbit)
"sudo python3 BW_limit.py -f del"     (to free the NIC)

# python getNetworkStatus.py
Routing Gateway:               10.6.28.254
Routing NIC Name:              eth0
Routing NIC MAC Address:       06:7f:12:00:00:15
Routing IP Address:            10.6.28.28
Routing IP Netmask:            255.255.255.0
"""
import os
import sys
import subprocess
import argparse


def capture_NIC_information():
    print("Start to capture the ip information!\n")
    routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

    for interface in netifaces.interfaces():
        if interface == routingNicName:
            # print netifaces.ifaddresses(interface)
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            except KeyError:
                pass


    print("ip information as follow:")
    display_format = '%-30s %-20s'
    print(display_format % ("Routing Gateway:", routingGateway))
    print(display_format % ("Routing NIC Name:", routingNicName))
    print(display_format % ("Routing NIC MAC Address:", routingNicMacAddr))
    print(display_format % ("Routing IP Address:", routingIPAddr))
    print(display_format % ("Routing IP Netmask:", routingIPNetmask))

    return routingNicName


print("\n###############BandWidth limit start!##############\n")

try:
    import netifaces
    routingNicName = capture_NIC_information()
except ImportError:
    try:
        command_to_execute = "pip install netifaces || easy_install netifaces"
        os.system(command_to_execute)
    except OSError:
        print("Can NOT install netifaces, Aborted!")
        sys.exit(1)
    finally:
        try:
            import netifaces
            routingNicName = capture_NIC_information()
        except:
            print("Error, netifaces module install fail! So, use the Default set: eth0 !")
            routingNicName = 'eth0'

parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--bandwidth', '-b', help='bandwidth, 设定本机带宽限制')
parser.add_argument('--flag', '-f', help='flag, 设定执行模式：build——带宽限制设定；del——清除带宽限制')
args = parser.parse_args()

try:
    flag =  args.flag
except:
    print("Error! You should give me the operation flag that you neet!")
    sys.exit(1)


try:
    if flag == "build":
        print("\n*****Now start to limit BandWidth!*****")
        BandWidth_set = args.bandwidth
        cmd1 = "tc qdisc add dev %s root handle 1: htb default 20" % routingNicName
        cmd2 = "tc class add dev %s parent 1:0 classid 1:1 htb rate %sMbit" %(routingNicName, BandWidth_set)
        cmd3 = "tc class add dev %s parent 1:1 classid 1:20 htb rate %sMbit ceil %sMbit" %(routingNicName, BandWidth_set, BandWidth_set)
        cmd = cmd1+" && "+cmd2+" && "+cmd3
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        if p.poll() == 0:
            print("\n##########BandWidth limit is success, value is BandWidth_set %sMbit!##########\n" % BandWidth_set)
        else:
            print("Error! Can not limit BandWdith. Please check your device!")
    elif flag == "del":
        print("\n*****Now start to del the limit!*****")
        cmd = "tc qdisc del dev %s root" % routingNicName
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        if p.poll() == 0:
            print("\n#########BandWidth limit del is success!##########\n")
        else:
            print("Error! Can not del the limit. Please check if this NIC was limited!")
            sys.exit(1)
    else:
        raise ValueError('Operation flag must be the "build" or "del"!')
except:
    raise ValueError('Error! Check the NIC(default) set!')