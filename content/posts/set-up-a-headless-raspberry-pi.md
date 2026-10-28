---
title: "Set Up A Headless Raspberry Pi"
date: 2018-10-04T21:38:41-04:00
slug: "set-up-a-headless-raspberry-pi"
url: /2018/10/04/set-up-a-headless-raspberry-pi/
author:
  - "jhowe"
year: ["2018"]
month: ["2018-10"]
categories:
  - "linux"
tags: []
aliases:
  - "/2018/10/04/set-up-a-headless-raspberry-pi/feed/"
---

I find myself setting up Raspberry Pi’s more frequently than I’d like. I never ever have a monitor connected. Below is the method I use to get wireless network connectivity without connecting an Ethernet cable or a monitor and keyboard. This is here because I’m tired of sifting through incorrect articles to find this information.

<!--more-->

1. Download Raspbian and flash it to your SD card. Plenty of good guides out there, [but there’s nothing quite like the source](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
2. Mount the SD card to your machine and navigate to the boot directory
3. Create a blank file called “ssh” in the root of the boot partition
4. Create a new file called “wpa\_supplicant.conf” and include the contents below. Replace [ssid] and [password] with the values pertaining to your network.
5. Safely unmount, and have fun!

```text
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev

update_config=1
country=US

network={
ssid="[ssid]"
psk="[password]"
key_mgmt=WPA-PSK
}
```

If you want more information on this process – check out the [Raspbian documentation on a headless install](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md), and the [wpa\_supplicant documentation](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md).

Until next time,

Jon
