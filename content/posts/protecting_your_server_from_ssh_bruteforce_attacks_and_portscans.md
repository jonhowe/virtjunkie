---
title: "Protecting Your Server From SSH Bruteforce Attacks and Portscans"
date: 2006-05-05T16:26:23-04:00
slug: "protecting_your_server_from_ssh_bruteforce_attacks_and_portscans"
url: /2006/05/05/protecting_your_server_from_ssh_bruteforce_attacks_and_portscans/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-05"]
categories:
  - "security"
tags: []
aliases:
  - "/2006/05/05/protecting_your_server_from_ssh_bruteforce_attacks_and_portscans/feed/"
---

First of all, this entry is not being entered in Drupal 4.7, I haven’t had the time to get that set up yet.

The other day I decided to take a look at my server logs, which is something that I should have been doing all along. I found out that more than one host has been brute force / dictionary scanning my ssh server. I decided that even though my passwords are strong, that I really didn’t want people to have the ability to do that. Fortunately for me there are some tools out there that work great for this very purpose. The one that I chose is called [DenyHosts](http://denyhosts.sourceforge.net/).

Basically how denyhosts works is it scans your security log (there are several options as to what distro type) for different strings, and if more than X number of failed access attempts occur the attacking host is added to your hosts.deny file.

Now, this functionality is found in a number of programs. The great thing about denyhosts is that (optionally) every hour your list is synchronized with a server so that you’re protection is increased greatly.

I used [this tutorial](http://howtoforge.net/preventing_ssh_dictionary_attacks_with_denyhosts) to install it on my computer. The only change that I would make to it is to use denyhosts 2.4 instead of 2.0, which can be found at the [denyHosts](http://denyhosts.sourceforge.net/) site.

I got started on security and I didn’t want to stop quite yet. I also set up a portscan detector that blocks hosts that portscan you with iptables. It’s called portsentry, and can be installed with apt using:  
`apt-get install portsentry`.

I set up both of these utilities to email me immediately when an event occurs.

One note that I should add is that when I set up denyhosts for the first time it parsed through my existing security log and found that my current address had more than the threshold of incorrect passwords, so it blocked me from making a ssh connection to my server. To fix this just make sure that you check through your security log and make sure that you have less than the maximum amount of denied login attempts before you terminate the ssh connection.

As always, if you have any questions email me at howe -dot- jon -at- gmail -dot- com.

Later,  
Jon Howe
