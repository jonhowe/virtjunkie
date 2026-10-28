---
title: "Don’t let your daemons die"
date: 2006-02-23T21:30:03-05:00
slug: "dont_let_your_daemons_die"
url: /2006/02/23/dont_let_your_daemons_die/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-02"]
categories:
  - "servers"
tags: []
aliases:
  - "/2006/02/23/dont_let_your_daemons_die/feed/"
---

Okay, let’s pretend that this isn’t the first time that I’ve posted in about a month. School really has been crazy. I haven’t really even had time to do anything new or cool lately. Tonight though, I’m putting school aside.

I’ve been having some problems with one of the daemons on one of my server’s randomly dying on me, and it got to the point that I couldn’t bear it anymore, I had to find a solution.

Thankfully, people have been using developing things for unix/linux for longer than I’ve been alive, and there’s a program that acts as a perfect band-aid. It’s called **Monitor**.

Get the file:  
**apt-get install monit**

Create the monit control file:  
(The monit control file uses a language of it’s own, if you want to learn it, feel free to go to the references at the bottom of this page. Otherwise just use some form of the file below)

`check process sshd with pidfile /var/run/sshd.pid  
start program "/etc/init.d/sshd start"  
stop program "/etc/init.d/sshd stop"  
if failed port 22 protocol ssh then restart  
if 5 restarts within 5 cycles then timeout`

Then, on the console type **monit -c [path to the above file] -d [number of seconds inbetween checks]**

This this is saving me a lot of trouble.

Sources:  
  
http://www.tildeslash.com/monit/doc/examples.php  
http://www.tildeslash.com/monit/  
http://www.tildeslash.com/monit/doc/manual.php  
  
Hopefully it wont be another month,  
Jon Howe
