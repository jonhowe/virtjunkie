---
title: "SSH Local Port Forwarding Made Easy"
date: 2007-03-14T16:03:07-04:00
slug: "ssh-local-port-forwarding-made-easy"
url: /2007/03/14/ssh-local-port-forwarding-made-easy/
author:
  - "jhowe"
year: ["2007"]
month: ["2007-03"]
categories:
  - "linux"
  - "security"
  - "servers"
tags: []
aliases:
  - "/2007/03/14/ssh-local-port-forwarding-made-easy/feed/"
---

I’ve been using this for a while now, and have found it a great little trick for accessing services that are blocked due to a firewall.

It’s pretty simple, you just have a few parts to the command string.  The first command argument tells ssh to forward a local port (LP) to a remote machine Remote) on a remote port (RP).  The second part is something you’re probably familiar with, the destination that you’re connecting to (Destination).

An example with the abbreviations above would be:

```bash
ssh -L LP:Remote:RP Destination
```

Say for example, you ran the command “ssh -L 1234:myInternalServer.com:80 myExternalServer”.  In order to access port 80 on myInternalServer.com you’d open up your web browser and point it to http://localhost:1234.  It’s as easy as that!
