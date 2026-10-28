---
title: "How to Use the Tor Network for Application Anonymity"
date: 2006-01-02T01:54:21-05:00
slug: "how_to_use_the_tor_network_for_application_anonymity"
url: /2006/01/02/how_to_use_the_tor_network_for_application_anonymity/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-01"]
categories:
  - "security"
tags: []
aliases:
  - "/2006/01/02/how_to_use_the_tor_network_for_application_anonymity/feed/"
---

The [Tor Network](http://tor.eff.org/) uses something called [Onion Routing](http://en.wikipedia.org/wiki/Onion_Routing). Tor’s functionality is pretty simple. You run a daemon on a computer on your network (the tor client) and it connects to a server inside the tor network. Once your transmitted packets are inside the tor network they are routed through the different servers in a way so that no server knows the complete path that a packet takes. On top of this, all transmission inside the tor network is encrypted in order to prevent [Man in the Middle Attacks](http://en.wikipedia.org/wiki/Man_in_the_middle).

The network is not easily accessed directly though. The easiest way to utilize tor as a functional service for your network is to use something called [Privoxy](https://www.privoxy.org/). Privoxy acts as a middleman between tor and the computers on your network.

We’ll talk more about the configuration of these later, but first we need to install them.

I’m going to assume, as usual, that you’re Debian as your distribution.

**Note: I had some problems getting tor to install properly with apt. In order to fix this I needed to add the following lines to my /etc/apt/sources.list file:  
testing**

**deb http://ftp.egr.msu.edu/debian/ testing main non-free contrib**

**deb-src http://ftp.egr.msu.edu/debian testing main non-free contrib**

**I also added the following lines to my /etc/apt/prefrences file to make it so that apt doesn’t try to get packages from the testing branch all of the time:**

**Package: \*  
Pin: release a=testing  
Pin-Priority: 999**

Stay tuned for a tutorial on how to use the previous process, which is called apt pinning.

Next we install Privoxy and Tor using the following command:  
`apt-get -t testing tor privoxy`

Now add the following line to your **/etc/privoxy/config**:  
`forward-socks4a / localhost:9050 .`

If you’re installing this on your own computer then you can leave this as it is. Otherwise change the `listen-address from 127.0.0.1 to the ip address that the interface that goes to the network uses. This line reads: listen-address 192.168.3.2:8118 in my config file.`

Now just start the daemons:  
`/etc/init.d/tor start`  
`/etc/init.d/privoxy start`

All that’s left is configuring your applications to use the proxy. Every app has different methods of using a proxy, and some don’t even have a way to access a proxy. If you’re trying to run something like firefox anonymously, then just go to **connection settings** and change the **Http Proxy** and the **Https Proxy** to the IP address and the port that privoxy is running on. If you want to use something like Aol Instant Messenger you can use tor directly by going into the settings and changing the **Socks 4** proxy to the IP address that tor is running on and the port number 9050.

After doing this all connections will be running through the anonymous tor network. If you have any questions feel free to leave me a comment, and I will answer.

Later,  
Jon Howe
