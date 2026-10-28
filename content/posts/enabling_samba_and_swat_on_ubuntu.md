---
title: "Enabling Samba and SWAT on Ubuntu"
date: 2006-07-06T07:37:12-04:00
slug: "enabling_samba_and_swat_on_ubuntu"
url: /2006/07/06/enabling_samba_and_swat_on_ubuntu/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-07"]
categories:
  - "linux"
  - "servers"
tags: []
aliases:
  - "/2006/07/06/enabling_samba_and_swat_on_ubuntu/feed/"
---

I recently got an album from [AllOfMP3.com](http://www.allofmp3.com/) on my laptop while I was away from my house, and wanted it on my desktop computer. In the past I’ve used Samba to transfer from Windows to Linux, so that’s what I did this time.

There were a couple of problems though, i didn’t have samba installed or configured because I just switched from Ubuntu Breezy to Ubuntu Dapper. Samba can be a bit of a pain to set up by hand, so that’s why I use SWAT (Samba Web Administration Tool).

SWAT doesn’t work automatically in ubuntu though, in order to get it to work the install the following packages if you’re using **inetd** (not recommended):

`apt-get install samba swat netkit-inetd  
sudo update-inetd --enable 'swat'`

Otherwise, if you’re using the recommended **xinetd** use the following fix:

Create a text file called ‘swat’ with the following information in it:

`# default: on  
# description: SWAT - The Samba Web Administration Toolkit  
service vmware-authd  
{  
disable = no  
port = 901  
socket_type = stream  
protocol = tcp  
wait = no  
user = root  
server = /usr/sbin/swat  
type = unlisted  
}`  
Then restart either (x)inetd and in your browser goto http://localhost:901 to log in.

That should work, if it doesn’t email me at howe dot jon -at- gmail \_dot\_ com
