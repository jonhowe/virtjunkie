---
title: "ESXi 5.1 – Regain Access to Host After Setting Wrong Default Gateway"
date: 2013-03-15T16:56:03-04:00
slug: "esxi-5-1-regain-access-to-host-after-setting-wrong-default-gateway"
url: /2013/03/15/esxi-5-1-regain-access-to-host-after-setting-wrong-default-gateway/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-03"]
categories:
  - "servers"
  - "vmware"
tags: []
aliases:
  - "/2013/03/15/esxi-5-1-regain-access-to-host-after-setting-wrong-default-gateway/feed/"
---

I’ll admit – I’ve done this once or twice. Each time causes me some grief while trying to get things set up correctly.

Here’s how to fix this issue as long as you have access to the Direct Console UI or ESXi Shell.

<!--more-->

  
[text]  
esxcli network ip route ipv4 remove -g w.x.y.z -n default  
esxcli network ip route ipv4 add -g a.b.c.d -n default  
[/text]  
This assumes that w.x.y.z is the old, incorrect gateway, that you might have set in the vSphere client, and a.b.c.d is the new gateway.
