# mac-on-lan-to-webhook
Trigger a remote webhook when it detect a device (MAC Address) in your LAN.

This repository contains the code to be able to run a Docker container that trigger a remote webhook when it detect a device (MAC Address) in your LAN.
For example, you can trigger to a IFTTT Webhook (https://ifttt.com/maker_webhooks) when it detect your smartphone is connected to your home WiFi network.

I personally use this docker container to turn on some Yeelight bulbs by pressing Amazon Dash buttons. Sadly Amazon has abandoned the Amazon-dash buttons, but thankfully I was able to get them back thanks to this guide from Christopher Mullins: https://blog.christophermullins.com/2019/12/20/rescue-your-amazon-dash-buttons/ 

It is important to remember that to detect the MAC (the ARP Probe), the docker container and the device we want to detect must be on the same network. In that sense, it is important to execute the container with the macvlan type network (which we will have to create first) instead of the bridge or host networks.

More info about macvlan (not supported on windows) here: https://docs.docker.com/network/macvlan/ 

I would like to specify that _I am Not a developer_ as I do it all for hobby as is my passion and in my little free time.

## Information you need to provide before you start ##

### You need docker to build and run the container ###

You can get docker from here: https://docs.docker.com/get-docker/

### You need to provide info of your devices ###

You need to provide the following associated information: 
 - The device 1: MAC address, device name, and webhook url.
 - The device 2: MAC address, device name, and webhook url.
 - The device 3: MAC address, device name, and webhook url.

## How to start ##

1. Clone this repo: `git clone https://github.com/leandroteleco/mac-on-lan-to-webhook`
2. Build the docker: `docker build -t mac-on-lan-to-webhook .`
3. Run the docker:
 - With full command: `docker run -it -e DEVICE_1_MAC=000000000000 -e DEVICE_1_NAME=DEVICE1-SMARTPHONE -e DEVICE_1_WEBHOOK=https://maker.ifttt.com/trigger/ -e EVENT_NAME_FOR_DEVICE_1/with/key/YOUR_IFTTT_KEY -e DEVICE_2_MAC=FFFFFFFFFFFF -e DEVICE_2_NAME=DEVICE2-TABLET -e DEVICE_2_WEBHOOK=https://maker.ifttt.com/trigger/ -e EVENT_NAME_FOR_DEVICE_2/with/key/YOUR_IFTT_KEY -e DEVICE_3_MAC=123456123456 -e DEVICE_3_NAME=DEVICE3-PC -e DEVICE_3_WEBHOOK=https://maker.ifttt.com/trigger/EVENT_NAME_FOR_DEVICE_3/with/key/YOUR_IFTT_KEY-d mac-on-lan-to-webhook`
 - With a file with environment variables and command:
   - Write a file (you can name it whatever you want, but I suggest ".env") with all environment variables:

```
DEVICE_1_MAC=000000000000
DEVICE_1_NAME=DEVICE1-SMARTPHONE
DEVICE_1_WEBHOOK=https://maker.ifttt.com/trigger/EVENT_NAME_FOR_DEVICE_1/with/key/YOUR_IFTTT_KEY

DEVICE_2_MAC=FFFFFFFFFFFF
DEVICE_2_NAME=DEVICE2-TABLET
DEVICE_2_WEBHOOK=https://maker.ifttt.com/trigger/EVENT_NAME_FOR_DEVICE_2/with/key/YOUR_IFTT_KEY

DEVICE_3_MAC=123456123456
DEVICE_3_NAME=DEVICE3-PC
DEVICE_3_WEBHOOK=https://maker.ifttt.com/trigger/EVENT_NAME_FOR_DEVICE_3/with/key/YOUR_IFTT_KEY
```

   - Run the docker with this command: `docker run -it --env-file .env -d mac-on-lan-to-webhook`
