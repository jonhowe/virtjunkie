---
title: "SSH Auto Login Using Putty"
date: 2013-02-09T22:17:18-05:00
slug: "ssh-auto-login-using-putty"
url: /2013/02/09/ssh-auto-login-using-putty/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-02"]
categories:
  - "featured"
  - "scripting"
  - "automation"
  - "servers"
  - "vmware"
tags: []
aliases:
  - "/2013/02/09/ssh-auto-login-using-putty/feed/"
---

I once had a person tell me that the most successful individuals in IT are lazy.  Years after hearing that, the notion has stuck with me and translates into much of how I attach problems.

If you’re like me, you use putty to connect to servers via SSH frequently. Now, I know that you can use key based authentication using puttygen, but in the scenario that you don’t want to go that route, you can use the method below to create windows shortcuts to automatically log into a host using putty.

<!--more-->

In my scenario, I have a few VMware ESXi hosts that I connect to pretty frequently, and logging in over and over gets annoying.

This solution is really quite simple. All you need to do is create a shortcut to this [Example Batch File](http://db.tt/GrmFD3L9). Make sure you edit the file to include your username and password.  Disclaimer – hard coding your password in plain text is generally considered bad security practice. Only do this if you know what you’re doing.

Modify the properties of each shortcut, and change the “Target” field of each one.  Here’s what one of mine looks like:

“C:\VMware Shortcuts\auto-ssh.bat” corp-esx-01

Here’s the breakdown of the batch file:

( -ssh ) – connect to the host using SSH

( -l [USERNAME] ) – configures putty to use a username

( -pw [PASSWORD] ) – configures putty to use a password

( %1) – since this is a batch file, %1 is will be replaced with the first parameter provided when the script is run.  Adding the name of your server onto the end of a windows shortcut will achieve this goal.

In order to make the shortcut a little bit more visually appealing, I created an ICO file to give the shortcut. I’ve provided it below.

[![](http://db.tt/CFHL4UZ0)](http://db.tt/CFHL4UZ0)

Example VMware Icon
