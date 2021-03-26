#!/usr/bin/env python3

import os
import requests
import json
import time
import socket
import struct
import binascii

# DEVICE 1
DEVICE_1_MAC = os.environ.get('DEVICE_1_MAC').upper()
DEVICE_1_NAME = os.environ.get('DEVICE_1_NAME')
DEVICE_1_WEBHOOK = os.environ.get('DEVICE_1_WEBHOOK')

# DEVICE 2
DEVICE_2_MAC = os.environ.get('DEVICE_2_MAC').upper()
DEVICE_2_NAME = os.environ.get('DEVICE_2_NAME')
DEVICE_2_WEBHOOK = os.environ.get('DEVICE_2_WEBHOOK')

# DEVICE 3
DEVICE_3_MAC = os.environ.get('DEVICE_3_MAC').upper()
DEVICE_3_NAME = os.environ.get('DEVICE_3_NAME')
DEVICE_3_WEBHOOK = os.environ.get('DEVICE_3_WEBHOOK')

macs = {
    DEVICE_1_MAC : DEVICE_1_NAME,
    DEVICE_2_MAC : DEVICE_2_NAME,
    DEVICE_3_MAC : DEVICE_3_NAME
}

def trigger_webhook (my_webhook_url):
    url = my_webhook_url
    payload = "Payload=Payload"
    headers = {'Accept': 'application/json', 'Authorization': "Bearer " + "Bearer Token", 'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("GET", url, headers=headers, data=payload)
    #print("Response code: {}".format(response.status_code))
    if response.status_code != 200:
        print("ERROR: The error code is: {}".format(response.status_code))
        print("Response: " + response.text)
        #print (json.dumps(response.json(), indent=4, sort_keys=True))
    else:
        print("Response: " + response.text)
        #print (json.dumps(response.json(), indent=4, sort_keys=True))
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
    my_connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) # Just works on GNU/Linux!
    arp_code_protocol = 2054 # ARP Ethertype (0x0806) https://en.wikipedia.org/wiki/EtherType

    while True:
        raw_data, addr = my_connection.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        #print('Ethernet Frame: ' + 'Destination: {}, Source: {}, Protocol: {} / {}'.format( dest_mac, src_mac, eth_proto, socket.ntohs(eth_proto)))

        if socket.ntohs(eth_proto) != arp_code_protocol:
            continue

        # read out data 
        my_packet = my_connection.recvfrom(2048)
        my_arp_header = my_packet[0][14:42]
        my_arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", my_arp_header)
        my_source_mac = binascii.hexlify(my_arp_detailed[5]).decode('ascii').upper()
        my_source_ip = socket.inet_ntoa(my_arp_detailed[6])
        my_dest_ip = socket.inet_ntoa(my_arp_detailed[8])

        if my_source_mac in macs:

            if macs[my_source_mac] == DEVICE_1_NAME and my_source_ip == '0.0.0.0':
                print ("Device " + DEVICE_1_NAME + " with MAC " + my_source_mac + " and with IP " + my_source_ip + " is in the network.")
                trigger_webhook(DEVICE_1_WEBHOOK)
                
            if macs[my_source_mac] == DEVICE_2_NAME and my_source_ip == '0.0.0.0':
                print ("Device " + DEVICE_2_NAME + " with MAC " + my_source_mac + " and with IP " + my_source_ip + " is in the network.")
                trigger_webhook(DEVICE_2_WEBHOOK)

            if macs[my_source_mac] == DEVICE_3_NAME and my_source_ip == '0.0.0.0':
                print ("Device " + DEVICE_3_NAME + " with MAC " + my_source_mac + " and with IP " + my_source_ip + " is in the network.")
                trigger_webhook(DEVICE_3_WEBHOOK)
                

def main():
    sniff()

main()
