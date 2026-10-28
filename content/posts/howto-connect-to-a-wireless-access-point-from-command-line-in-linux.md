---
title: "Howto: Connect to a Wireless Access Point from Command Line in Linux"
date: 2006-11-06T13:50:47-05:00
slug: "howto-connect-to-a-wireless-access-point-from-command-line-in-linux"
url: /2006/11/06/howto-connect-to-a-wireless-access-point-from-command-line-in-linux/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-11"]
categories:
  - "linux"
tags: []
aliases:
  - "/2006/11/06/howto-connect-to-a-wireless-access-point-from-command-line-in-linux/feed/"
---

This took me a little time to figure out, so I thought I’d share it with you.

This assumes that you’re using a PCMCIA (PC Card), but it should mostly work if you are using [Ndiswrapper](http://ndiswrapper.sf.net/) too.

<!--more-->

In order to see what networks are available you need to do a scan with your pc card. I’m pretty sure that this shouldn’t work with the ndiswrapper drivers..

**sudo iwlist scan** should return a list of all of the available wireless networks that are broadcasting their SSID.

Then you have to connect to the network. Do this by checking the output of the previous command and see what it says next to security, or wep. If it says open, then you have it fairly easy command wise.

To connect to an open access point, enter the following commands:

**sudo iwconfig mode managed**

**sudo iwconfig**  **key off**

**sudo dhclient**   
To connect to an access point that is using wep encryption and you know the key enter the following commands:

sudo iwconfig mode managed

sudo iwconfig key

sudo dhclient   
I should specify that the above way of setting the key is meant to be used with a hex key. If you want to use a string key use the following command in place of the second command in the group above:

sudo iwconfig key s:

Hopefully this was helpful. Let me know if it was!

Jon
