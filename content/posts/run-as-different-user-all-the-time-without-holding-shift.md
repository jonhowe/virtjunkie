---
title: "Run As Different User (All the time, without holding shift!)"
date: 2013-02-12T00:17:19-05:00
slug: "run-as-different-user-all-the-time-without-holding-shift"
url: /2013/02/12/run-as-different-user-all-the-time-without-holding-shift/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-02"]
categories:
  - "automation"
  - "featured"
  - "servers"
  - "windows-server"
tags: []
aliases:
  - "/2013/02/12/run-as-different-user-all-the-time-without-holding-shift/feed/"
---

The title of this post has bothered me since… forever. I really don’t like to take extra steps for things I do on a regular basis…

<!--more-->

Opening AD Users and Computers is something that I open on a pretty regular basis, but I use this method on several different utilities.

In order to do this, you’ll have to modify the target field in the shortcut of your program to include the [runas](http://technet.microsoft.com/en-us/library/bb490994.aspx) command.

Example: Active Directory Users and Computers:

Original:    %SystemRoot%\system32\dsa.msc

Different User:    C:\Windows\System32\runas.exe /user:[domain]\user “mmc %windir%\system32\dsa.msc”
