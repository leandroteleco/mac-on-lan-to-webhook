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

def main():
    print("Starting the program: ")
    my_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003)) # Just works on GNU/Linux!
    try:
        while True:
            my_packet = my_socket.recvfrom(2048)
            my_ethernet_header = my_packet[0][0:14]
            my_ethernet_detailed = struct.unpack("!6s6s2s", my_ethernet_header)
            # skip non-ARP packets
            my_ethertype = my_ethernet_detailed[2]
            if my_ethertype != '\x08\x06':
                continue
            # read out data 
            my_arp_header = my_packet[0][14:42]
            my_arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", my_arp_header)
            my_source_mac = binascii.hexlify(my_arp_detailed[5])
            my_source_ip = socket.inet_ntoa(my_arp_detailed[6])
            my_dest_ip = socket.inet_ntoa(arp_detailed[8])
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

main()