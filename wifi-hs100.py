#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:30:03 2020

@author: hrishi
"""
import socket
import argparse
commands = { 'on':' {"system":{"set_relay_state":{"state":1}}}',
             'off':' {"system":{"set_relay_state":{"state":0}}}',
             'info':'{"system":{"get_sysinfo":{}}}'}


def encrypt(input):
    key=171
    result="\0\0\0\0"
    for i in input:
        a = key ^ ord(i)
        key = a
        result += chr(a)
    return result

def decrypt(input):
    key=171
    result="\0\0\0\0"
    for i in input:
        a = key ^ ord(i)
        key= ord(i)
        result +=chr(a)
    return result

parser = argparse.ArgumentParser()
parser.add_argument('-c','--command',required=True)
parser.add_argument('-i','--ip',required=True)
args = parser.parse_args()

encr=encrypt(commands[args.command])
print(args.command)
print(encr)
print(decrypt(encr))
print(args.ip)
ip=""
if (args.ip is None):
    ip="192.168.1.8"
else:
    ip=args.ip

port=9999
tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp.connect((ip,port))
tcp.send(encr)
data=tcp.recv(2048)
tcp.close()
print("printing return data")
print(decrypt(data))
