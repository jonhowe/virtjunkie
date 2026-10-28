---
title: "Craaaazy Stuff"
date: 2005-12-20T10:33:54-05:00
slug: "craaaazy_stuff"
url: /2005/12/20/craaaazy_stuff/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-12"]
categories:
  - "linux"
tags:
  - "computers"
  - "debian"
aliases:
  - "/2005/12/20/craaaazy_stuff/feed/"
---

So last night I decided to take windows off of my laptop. This probably should have been easy. However, when is anything ever easy? When I woke up this morning I found out that in the middle of the night, during my net-install, the network cord came unplugged.

Apparently when you unplug the network cable during a Debian Netinstall the installer stops downloading the remaining packages and sets up what you have.

As you can probably guess, this is a little problem. When I tried to start up KDE I got an X11 error. Trying to figure out what the deal was here was a pain, but I was able to fix it by uninstalling X11, KDE, and Gnome ( `apt-get remove x11r6-6`), kdm, and gdm. My goal here was to start with as fresh of a slate as I could.

After that I needed to get X11 and KDE back installed. To do this I just ran the follwing command (this takes a while, because it’s re-installing a lot of your operating system again.

`apt-get install x-server-xfree86 x-window-system x-window-system-core kdm`

That should work, but if you have problems leave a comment and I’ll get back to you ASAP.

Later,  
Jon Howe
