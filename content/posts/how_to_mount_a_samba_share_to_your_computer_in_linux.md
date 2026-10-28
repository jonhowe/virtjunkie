---
title: "How to Mount a Samba share to your Computer in Linux"
date: 2005-12-14T09:48:01-05:00
slug: "how_to_mount_a_samba_share_to_your_computer_in_linux"
url: /2005/12/14/how_to_mount_a_samba_share_to_your_computer_in_linux/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-12"]
categories:
  - "linux"
tags:
  - "samba"
aliases:
  - "/2005/12/14/how_to_mount_a_samba_share_to_your_computer_in_linux/feed/"
---

This is something that I’ve been wanting to do for some time. It’s just this morning that I actually decided to do it. It’s pretty simple.

This small tutorial is based upon the assumption that you already have a samba share set up. However, if you don’t, then keep posted, because I’ll talk about that in a later tutorial. Also, It’s based upon the assumption that you have the samba client and sambafs installed. In debian all that you have to do to install this is type in the following line:  
`apt-get install smbfs smbclient`

All that you have to do is type in the following command to have a non-permanent solution (on one line):  
`mount -t smbfs //[server ip or domain name]/[server directory] [place that you want to mount the directory] -o username=[samba username],password=[samba password]`

If you go with this solution you’ll have to reenter this command each time that you start up your computer. To make this a permanent change, you need to edit your ‘/etc/fstab’ file by adding the following line at the bottom (on one line)  
`//[server name or ip]/[shrae name] [directory to mount share into] smbfs username=[samba username],password=[samba password] 0 0`

This works for me, but if you have any problems feel free to leave a comment and I’ll help you out ASAP.

Later,  
Jon Howe
