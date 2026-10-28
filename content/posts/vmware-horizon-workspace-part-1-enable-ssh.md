---
title: "VMware Horizon Workspace – Part 1 – Enable SSH"
date: 2013-07-30T17:16:59-04:00
slug: "vmware-horizon-workspace-part-1-enable-ssh"
url: /2013/07/30/vmware-horizon-workspace-part-1-enable-ssh/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-07"]
categories:
  - "horizon-workspace"
  - "vmware"
tags: []
aliases:
  - "/2013/07/30/vmware-horizon-workspace-part-1-enable-ssh/feed/"
---

I’ve never met a VMware Admin who will use the console to access a VM if they have a choice. There are plenty of tutorials out there that will show you how to do this, but since I’m starting a series, I guess I’ll throw the same info on the internet, but put my own spin on it.

<!--more-->

This post is [part of a series showing](/2013/07/30/vmware-horizon-workspace-part-0-intro/ "part of a series showing") how to set up [VMware Horizon Workspace in a production](/2013/07/30/vmware-horizon-workspace-part-0-intro/ "VMware Horizon Workspace in a production") environment.

If copy and paste is disabled within the console (shame on you if it is…) enable it using [VMware KB1026437](http://kb.vmware.com/kb/1026437 "VMware KB1026437")

Paste the following line into the console of each virtual appliance:

```bash
sed -i.bak 's/PermitRootLogin no/PermitRootLogin yes/g' /etc/ssh/sshd_config;service sshd restart
```

Technically this is two commands, but you can paste the whole thing in. All it does is back up your current SSHD config file, replace the line that disallows root login with a line that does allow it, then restarts the service.

Bing bang boom, now you can use whatever ssh client you like to connect to your virtual appliances.
