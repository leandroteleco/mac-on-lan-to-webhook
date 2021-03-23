# mac-on-lan-to-webhook
Trigger a remote webhook when it detect a device (MAC Address) in your LAN.

This repository contains the code to be able to run a Docker container that trigger a remote webhook when it detect a device (MAC Address) in your LAN.
For example, you can trigger to a IFTTT Webhook when it detect your smartphone is connected to your home WiFi network.

## Information you need to provide before you start ##

### You need docker to build and run the container ###

You can get docker from here: https://docs.docker.com/get-docker/

### You need to provide info of your devices ###

You need to provide the following associated information: 
 - The device 1: MAC address, device name, and webhook url.
 - The device 2: MAC address, device name, and webhook url.


## How to start ##

1. Clone this repo: `git clone https://github.com/leandroteleco/mac-on-lan-to-webhook`
2. Build the docker: `docker build -t mac-on-lan-to-webhook .`
3. Run the docker:
 - With full command: `docker run -it -e DEVICE_1_MAC=000000000000 -e DEVICE_1_NAME=DEVICE1-SMARTPHONE -e DEVICE_1_WEBHOOK=https://maker.ifttt.com/trigger/ -e EVENT_NAME_FOR_DEVICE_1/with/key/YOUR_IFTTT_KEY -e DEVICE_2_MAC=FFFFFFFFFFFF -e DEVICE_2_NAME=DEVICE2-TABLET -e DEVICE_2_WEBHOOK=https://maker.ifttt.com/trigger/ -e EVENT_NAME_FOR_DEVICE_2/with/key/YOUR_IFTT_KEY -d mac-on-lan-to-webhook`
 - With a file with environment variables and command:
   - Write a file (you can name it whatever you want, but I suggest ".env") with all environment variables:

```
DEVICE_1_MAC=000000000000
DEVICE_1_NAME=DEVICE1-SMARTPHONE
DEVICE_1_WEBHOOK=https://maker.ifttt.com/trigger/EVENT_NAME_FOR_DEVICE_1/with/key/YOUR_IFTTT_KEY

DEVICE_2_MAC=FFFFFFFFFFFF
DEVICE_2_NAME=DEVICE2-TABLET
DEVICE_2_WEBHOOK=https://maker.ifttt.com/trigger/EVENT_NAME_FOR_DEVICE_2/with/key/YOUR_IFTT_KEY
```

   - Run the docker with this command: `docker run -it --env-file .env -d mac-on-lan-to-webhook`
