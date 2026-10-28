---
title: "VMware Horizon Workspace – Part 0 – Intro"
date: 2013-07-30T16:54:46-04:00
slug: "vmware-horizon-workspace-part-0-intro"
url: /2013/07/30/vmware-horizon-workspace-part-0-intro/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-07"]
categories:
  - "horizon-workspace"
  - "servers"
  - "vmware"
tags: []
aliases:
  - "/2013/07/30/vmware-horizon-workspace-part-0-intro/feed/"
---

I’ve been working with Horizon Workspace since it went GA in March. At this point in time, I’m happy to say that I’ve got Workspace set up in a production environment.

In this series, I will be covering how I configured each part of this suite. I would expect that this process will become exponentially easier as time goes on. One thing to note is that I will write these posts assuming that you are at least moderately familiar with linux and Workspace. I will not go into details on how to install packages, deploy the VA, use the web interface. Use Google if you’re looking for that boring stuff 🙂 Here we go!

<!--more-->

Due to the reliance that the business will put on the Workspace, my definition of Production is as follows:

1. Externally Accessible
   1. One URL to rule them all, both internal and external
2. [Load Balanced from within DMZ](/2013/08/01/vmware-horizon-workspace-part-2-configure-nginx-as-frontend-with-microsoft-ca/ "VMware Horizon Workspace – Part 2 – Configure Nginx as Frontend with Microsoft CA")
   1. Multiple Load Balancers – no single point of failure!
3. Multiple Virtual Appliances
   1. At LEAST 2 of every VA that comes with Workspace (Gateway, Connector, Service, Data)
4. [External Postres SQL Database](/2013/11/23/vmware-horizon-workspace-part-3-configure-vmware-vpostgres-external-database/ "VMware Horizon Workspace – Part 3 – Configure VMware vPostgres External Database")
5. [Third Party SSL Certificate](/2013/08/01/vmware-horizon-workspace-part-2-configure-nginx-as-frontend-with-microsoft-ca/ "VMware Horizon Workspace – Part 2 – Configure Nginx as Frontend with Microsoft CA")
   1. I used Godaddy, but if I had to do it again, I’d go with Verisign, or a more reputable CA. This should be fixed in Workspace 1.5, which should be released by the end of July.
6. Data is stored on NFS rather than on local vmdk

Throughout this (we’ll call it an adventure) I’ve learned a lot about the product.Most importantly, it’s become clear to me that this is not a product easily administered by a “VMware Admin”. Horizon Workspace is built on top of Suse Enterprise Linux 11, relies heavily on Zimbra for the data component, and uses nginx for everything else.

Sound like greek? Don’t panic, you can set up a good amount of Horizon Workspace without being a linux guru, however, imho, most of the things you’ll need to do in a production environment will require at least a moderate familiarity with the linux command line.
