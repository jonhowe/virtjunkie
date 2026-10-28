---
title: "HowTo Restore Grub Boot Password In Ubuntu Dapper"
date: 2006-10-06T03:32:24-04:00
slug: "howto-restore-grub-boot-password-in-ubuntu-dapper"
url: /2006/10/06/howto-restore-grub-boot-password-in-ubuntu-dapper/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-10"]
categories:
  - "linux"
  - "security"
tags: []
aliases:
  - "/2006/10/06/howto-restore-grub-boot-password-in-ubuntu-dapper/feed/"
---

A cardinal rule with computer security is that if you have physical access to a computer, you can pretty much do whatever your heart desires to it. Luckily, this includes removing the grub password from a linux box [so that you can restore the root password…](/blog/node/90)

Your best course of action in doing this is to download a bootable linux cd. [The one that I tested this with](http://www.remote-exploit.org/index.php/BackTrack) is a worthwhile download even if you’re just reading this for fun.

<!--more-->

There are x steps involved with removing grub passwords:

1. **Boot** Backtrack Live Cd
2. Log in, and navigate to the “**/mnt**” directory
3. Then go to the partition that corresponds to your hard drive (if you only have one hard drive it’s likely “**hda1**“, or “**/mnt/hda1**“
4. Within that directory, navigate to “boot/grub”, and open “**menu.lst**” in a text editor
5. Comment out all lines that start with “**password**“
6. Restart Computer, and enjoy a password-less grub bootloader.

Feel free to leave your mind in the comments and I’ll get back to you as soon as I can.

Jon
