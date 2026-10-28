---
title: "New Toy"
date: 2005-10-21T13:55:18-04:00
slug: "new_toy"
url: /2005/10/21/new_toy/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-10"]
categories:
  - "computers"
tags: []
aliases:
  - "/2005/10/21/new_toy/feed/"
---

So a few days ago my motherboard died, which stunk. Fortunately I have a laptop where I can do schoolwork, but that still doesn’t mean that I didn’t need to get a replacement motherboard.

So I went to [Newegg.com](http://www.newegg.com/) and bought a decent Asus one.

I’m using Debian GNU/Linux as my primary operating system, and before installing the new motherboard I was Sure (just like in Windows) that I’d have to reinstall the operating system in order for it to load.

I was wrong. Debian detected almost all of the hardware changes, and applied the changes for the first login after the motherboard installation.

The only problem was that I don’t have serial device support…. I don’t think.

The thing is, I don’t have any sda\* devices in /dev. If you know anything about Linux, you know that these are needed to mount flash drives, usb hard drives, and the like.

Oh well, I’ll go forum surfing, and hopefully find an answer.

Later,  
Jon Howe
