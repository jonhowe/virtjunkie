---
title: "NetApp – Unable To Delete Snapshots (Dependency: busy, backup[n], dump)"
date: 2013-03-19T19:00:05-04:00
slug: "netapp-unable-to-delete-snapshots-dependency-busy-backupn-dump"
url: /2013/03/19/netapp-unable-to-delete-snapshots-dependency-busy-backupn-dump/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-03"]
categories:
  - "featured"
  - "netapp"
tags: []
aliases:
  - "/2013/03/19/netapp-unable-to-delete-snapshots-dependency-busy-backupn-dump/feed/"
---

I came across this error when a NDMP backup of a large volume failed.

To isolate the exact error and resolve the issue, I ran the following commands:

<!--more-->

[text]  
snap list [volume name]  
backup status  
[/text]

Line one below shows all of the snapshots for the particular volume. In my case, the

ntap> backup status

[![backupStatus](/wp-content/uploads/2013/03/backupStatus-300x36.png)](/wp-content/uploads/2013/03/backupStatus.png)

ntap> snap list volume

(I edited the volume name)

[![snapList](/wp-content/uploads/2013/03/snapList.png)](/wp-content/uploads/2013/03/snapList.png)

To resolve this, run the following commands. They disable NDMP, and kill all active NDMP threads. As long as you’re not running any NDMP backups, this will not affect anything else on your filer.

[text]  
ndmpd off  
ndmpd killall  
ndmpd on  
[/text]
