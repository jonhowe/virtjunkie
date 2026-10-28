---
title: "How to Set up a Complete Transparent Filtering Proxy"
date: 2006-01-01T01:50:51-05:00
slug: "how_to_set_up_a_complete_transparent_filtering_proxy"
url: /2006/01/01/how_to_set_up_a_complete_transparent_filtering_proxy/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-01"]
categories:
  - "linux"
tags: []
aliases:
  - "/2006/01/01/how_to_set_up_a_complete_transparent_filtering_proxy/feed/"
---

**This tutorial works with squid versions < 2.6**

Many companies find proxy servers useful for a number of reasons. For example, if a company has fairly low bandwidth and needs a cheap way to streamline the distribution of frequently accessed content, a proxy server, such as squid will help a lot. Another use of a proxy server in the business world is for what I like to call, “Employee Management”. In other words, this is for companies that want to see what their employees are viewing on the internet. They can also be used by companies that have less than perfect infrastructures and need to have a way to take one connection to the internet and spread it to many computers.

Squid is great for the uses above and for other unmentioned uses, but when combined with a content filter called dansguardian the results are awesome.

Dansguardian is a content filtering proxy that integrates itself with squid. You can find information about Dansguardian [here](http://sourceforge.net/docman/display_doc.php?docid=27215&group_id=131757), and [here](http://www.dansguardian.org/).

These two things combined into something called a Transparent Proxy allow for much greater flexibility for administrators and end users. With a non-transparent proxy everything that accesses the internet needs to have HTTP proxy support, and needs to be configured by hand before it can be used. With transparent proxying the connections to port 80 (http) are automatically redirected from their original path and routed through the proxy. Don’t worry if this sounds confusing, the details aren’t really that important.

Now for the good part: How to install and configure this in Debian.

1. Do a Base Install of Debian:
2. This means that when you get into aptitude  
   just hit ‘q’ and exit out, becuase we’ll be installing everything manually

Install the packages using apt-get: `'apt-get install squid dansguardian vim ssh'`

- That should take a little while but should download everything that you’ll need.

Now we have to make it so that the proxy works in non-transparent mode.

1. To do this we have to edit the dansguardian configuration file located at `'/etc/dansguardian/dansguardian.conf'`.
2. Navigate to the section labeled ‘Network Settings’ and change ‘filterip’ to the ip address that’s on the network that you’re clients will be listening on.
3. At the top of the file comment out the word “UNCONFIGURED”
4. Save and quit the file by typing: `wq` (if you’re using vi)
5. Do some final configuration on dansguardian by entering the command `'dpkg-reconfigure dansguardian'`

Now we have dansguardian all set. All that’s left is getting squid set up for transparent proxying, entering the iptables rules, and setting it up to all be set up correctly each time that you restart your proxy server.

In the squid configuration file, which is located at `'/etc/squid/squid.conf'` add and/or edit the following lines to enable transparent proxying.  
`'  
httpd_accel_host virtual  
httpd_accel_port 80  
httpd_accel_with_proxy on  
httpd_accel_uses_host_header on  
'`  
Do a search in the squid config file for `'http_access deny all'` and change it to `http_access allow all`. This file should be customized more in the future. This configuration tells squid to use no discretion as to who uses the proxy. Setting this up is beyond the scope of this tutorial.

That finishes the configuration of Squid. Now just enter the following commands and you should be set on the firewall rules. Create this file in the directory `'/etc/init.d'`. We’ll assume that eth0 is the interface going to the internet and eth1 is the interface leading to the client network.

`#! /bin/sh`

# Set up IP FORWARDing and Masquerading  
echo “Setting up forwarding”  
iptables –table nat –append POSTROUTING –out-interface eth0 -j MASQUERADE  
iptables –append FORWARD –in-interface eth1 -j ACCEPT  
echo 1 > /proc/sys/net/ipv4/ip\_forward

#enable transparent proxying  
echo “Enabling Transparent Proxying”  
iptables -t nat -A PREROUTING -i eth2 -p tcp –dport 80 -j REDIRECT –to-port 8080  
The first group of commands tells your system to take all of the packets that are going to the internet (eth0) and move them from the local interface (eth1) through the proxy server and on to the internet.

The second command does the transparent proxying. It listens for connections going to port 80 and redirects them to port 8080 (the dansguardian port) which in turn checks to see if the website is authorized. If it is the request is forwarded to squid, and then to the destination website. The process is pretty much the same, but opposite on the way back to the client.

The files in the script that we created need to be executed for the proxy to work, so what we’ll do is have it run on startup.

1. Make it executable: `'chmod +x /etc/init.d/local'`
2. Then make it run when the system starts up: `' update-rc.d local defaults 80'`

After that whole process you should have a fully functioning transparent content filtering proxy. If you have any comments / corrections / or suggestions feel free to leave a comment and I will answer.

Later,  
Jon Howe
