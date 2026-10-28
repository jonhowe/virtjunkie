---
title: "Chkconfig like program in Debian"
date: 2005-12-16T08:05:46-05:00
slug: "chkconfig_like_program_in_debian"
url: /2005/12/16/chkconfig_like_program_in_debian/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-12"]
categories:
  - "debian"
tags: []
aliases:
  - "/2005/12/16/chkconfig_like_program_in_debian/feed/"
---

I started out in Linux using Fedora, which is Redhat based. One of the indespensible tools that I used was called chkconfig. Basically what chkconfig does in Redhat based systems is allow the user to control what daemons start at boot time. This is useful for starting that annoying daemon that you always need or stopping the pesky one that always bothers you.

I used this a ton, and then I switched to Debian, and my whole world turned upside down. (some exaggeration intended)

Until recently I had no idea how to do this, until I found out about a little gem called ‘rcconf’.

Rcconf even has a little optional graphical display that you can use to manually select things to autostart or stop, which is helpful if you don’t know what it is you’re looking for.

If you’re on a pretty new installation of Debian you probably don’t have this yet, but you can get it by entering `apt-get install rcconf` into the console as root.

More Later,  
Jon Howe
