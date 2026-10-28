---
title: "How To Cache Apt Packages On A Network Using Apt-Cacher"
date: 2006-01-10T18:06:41-05:00
slug: "how_to_cache_apt_packages_on_a_network_using_apt-cacher"
url: /2006/01/10/how_to_cache_apt_packages_on_a_network_using_apt-cacher/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-01"]
categories:
  - "debian"
  - "linux"
  - "servers"
tags: []
aliases:
  - "/2006/01/10/how_to_cache_apt_packages_on_a_network_using_apt-cacher/feed/"
---

If you’ve got more than one computer running Debian that packages are downloaded through apt, then apt-cacher should help you a lot.

Apt-cacher is actually a cgi script that is run by apache. Using apt-cacher is very easy, and installing it is even easier.

**Step 1: Install apt-cacher.**  
(Run this on the proxy computer)

`apt-get install apt-cacher`

Enter the webpage : **http://localhost/apt-cacher**  
to see that the proxy is running.

**Step 2: Backup and Convert Clients sources.list.**  
(Do this on the computers that you want to access the cache.)

`cp /etc/apt/sources.list /etc/apt/sources.list.backup`

`vi /etc/apt/sources.list`

Press ‘:’ while in vi.

Enter “`%s/http:///http://[Your Proxy IP]/apt-cacher?//g`”

This searches through your sources and adds http://[Your Proxy IP]/apt-cacher?/ before every repository.

An example from my sources.list looks like this:

`deb http://192.168.3.2/apt-cacher?/www.backports.org/debian/ sarge-backports main`

**Step 3: Update Clients**

`apt-get update`

**Optional Step 4: Import Existing packages into the apt-cacher cache**

Copy the desired packages to the proxy directory **/var/cache/apt-cacher/import**

Run the import script to make it so that apt-cacher can use them.  
`perl /usr/share/apt-cacher/apt-cacher-import.pl`

**Step 5: Use apt-get**

If the required previous steps completed successfully you should now be able to use apt with it’s connection proxied through your apt-cacher proxy.

Questions / Comments, leave me a comment, and I’ll reply.

Later,  
Jon Howe
