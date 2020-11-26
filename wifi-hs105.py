#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:30:03 2020

@author: hrishi
"""
import socket
import argparse
import struct
commands = { 'on':'{"system":{"set_relay_state":{"state":1}}}',
             'off':'{"system":{"set_relay_state":{"state":0}}}',
             'info':'{"system":{"get_sysinfo":{}}}'}


def encrypt(input:str) ->bytes:
    key=171
    plainbytes=input.encode()
    buffer=bytearray(struct.pack(">I",len(plainbytes)))
    for i in plainbytes:
        a = key ^ i
        key = a
        buffer.append(a)
    return bytes(buffer)

def decrypt(input:bytes) ->str:
    key=171
    #buffer=bytearray(struct.unpack(">I",len(input)))
    buffer=[]
    for i in input:
        a = key ^ i
        key= i
        buffer.append(a) 
    plaintext=bytes(buffer)
    return plaintext.decode()

parser = argparse.ArgumentParser()
parser.add_argument('-c','--command',required=True)
parser.add_argument('-i','--ip',required=True)
args = parser.parse_args()

encr=encrypt(commands[args.command])
print(args.command)
print(encr)
print(decrypt(encr[4:]))

if (args.ip is None):
    ip="192.168.1.4"
else:
    ip=args.ip

port=9999
tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp.connect((ip,port))
tcp.send(encr)
data=tcp.recv(4096)
tcp.close()
print("printing return data")
print(decrypt(data[4:]))
mybyte=str.encode("hello")
btarr=bytearray(struct.pack(">I",len(mybyte)))
print(bytes(btarr))