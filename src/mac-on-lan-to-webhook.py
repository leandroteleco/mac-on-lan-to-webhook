#!/usr/bin/env python3

import os
import requests
import json
import time
import socket
import struct
import binascii

# DEVICE 1
DEVICE_1_MAC = os.environ.get('DEVICE_1_MAC')
DEVICE_1_NAME = os.environ.get('DEVICE_1_NAME')
DEVICE_1_WEBHOOK = os.environ.get('DEVICE_1_WEBHOOK')

# DEVICE 2
DEVICE_2_MAC = os.environ.get('DEVICE_2_MAC')
DEVICE_2_NAME = os.environ.get('DEVICE_2_NAME')
DEVICE_2_WEBHOOK = os.environ.get('DEVICE_2_WEBHOOK')

macs = {
    DEVICE_1_MAC : DEVICE_1_NAME,
    DEVICE_2_MAC : DEVICE_2_NAME
}

def trigger_webhook (my_webhook_url):
    url = my_webhook_url
    payload = {"Payload" : "Payload"}
    headers = {'Accept': 'application/json', 'Authorization': "Bearer " + "Bearer Token", 'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print("ERROR: The error code is: {}".format(response.status_code))
        print("Response: " + str(response.json()))
    else:
        print("Response: " + str(response.json()))
    return response

# Unpack ethernet frame
def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[:14]

#Return properly formatted MAC address (ie: AA:BB:CC:DD:EE:FF)
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    mac_addr = ':'.join(bytes_str).upper()
    return mac_addr

def sniff():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) # Just works on GNU/Linux!
    arp_code_protocol = 2054 # ARP Ethertype (0x0806) https://en.wikipedia.org/wiki/EtherType
    while True:
        raw_data, addr = conn.recvfrom(65536)
        my_packet = conn.recvfrom(2048)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        print('Ethernet Frame: ' + 'Destination: {}, Source: {}, Protocol: {} / {}'.format( dest_mac, src_mac, eth_proto, socket.ntohs(eth_proto)))
        if socket.ntohs(eth_proto) != arp_code_protocol:
            #print('my_ethertype: {}'.format(arp_code_protocol)) 
            continue
        # read out data 
        my_arp_header = my_packet[0][14:42]
        my_arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", my_arp_header)
        my_source_mac = binascii.hexlify(my_arp_detailed[5])
        my_source_ip = socket.inet_ntoa(my_arp_detailed[6])
        my_dest_ip = socket.inet_ntoa(my_arp_detailed[8])
        print ("Unknown MAC " + get_mac_addr(my_source_mac) + " from IP " + my_source_ip)
        if my_source_mac in macs:
            #print "ARP from " + macs[source_mac] + " with IP " + source_ip
            if macs[my_source_mac] == DEVICE_1_NAME:
                trigger_webhook(DEVICE_1_WEBHOOK)
            if macs[my_source_mac] == DEVICE_2_NAME:
                trigger_webhook(DEVICE_2_WEBHOOK)
        else:
            print ("Unknown MAC " + get_mac_addr(my_source_mac) + " from IP " + my_source_ip)

def test():
    print("Starting the program: ")
    try:
        #print('Going to create socket...')
        my_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003)) # Just works on GNU/Linux!
        #print('... socket created! :)')
    except socket.error as msg:
        print('Socket could not be created -> Error code {}, Message: {}'.format(msg[0],msg[1]))

    try:
        while True:
            #print('Going to create packet...')
            my_packet = my_socket.recvfrom(2048)
            #print('... packet created! :)')
            my_ethernet_header = my_packet[0][0:14]
            my_ethernet_detailed = struct.unpack("!6s6s2s", my_ethernet_header)
            # skip non-ARP packets
            my_ethertype = my_ethernet_detailed[2]
            
            print('Ethernet Frame: ' + 'Destination: {}, Source: {}, Protocol: {} '.format( my_ethernet_detailed[0], my_ethernet_detailed[1], my_ethertype))
            arp_code_protocol = 'b\'\x08\x06\''
            if str(my_ethertype) != arp_code_protocol:
                print('my_ethertype: {}'.format(arp_code_protocol)) 
                continue
            # read out data 
            my_arp_header = my_packet[0][14:42]
            my_arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", my_arp_header)
            my_source_mac = binascii.hexlify(my_arp_detailed[5])
            my_source_ip = socket.inet_ntoa(my_arp_detailed[6])
            my_dest_ip = socket.inet_ntoa(arp_detailed[8])
            print ("Unknown MAC " + my_source_mac + " from IP " + my_source_ip)
            if my_source_mac in macs:
                #print "ARP from " + macs[source_mac] + " with IP " + source_ip
                if macs[my_source_mac] == DEVICE_1_NAME:
                    trigger_webhook(DEVICE_1_WEBHOOK)
                if macs[my_source_mac] == DEVICE_2_NAME:
                    trigger_webhook(DEVICE_2_WEBHOOK)
            else:
                print ("Unknown MAC " + my_source_mac + " from IP " + my_source_ip)
   
    except KeyboardInterrupt:
        print("Press Ctrl-C to terminate while statement")
        pass

def main():
    sniff()

main()