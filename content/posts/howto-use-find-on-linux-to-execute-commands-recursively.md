---
title: "HowTo:  Use Find on Linux to Execute Commands Recursively"
date: 2007-01-11T03:07:18-05:00
slug: "howto-use-find-on-linux-to-execute-commands-recursively"
url: /2007/01/11/howto-use-find-on-linux-to-execute-commands-recursively/
author:
  - "jhowe"
year: ["2007"]
month: ["2007-01"]
categories:
  - "linux"
tags: []
aliases:
  - "/2007/01/11/howto-use-find-on-linux-to-execute-commands-recursively/feed/"
---

I just used [the best music player on the planet](http://amarok.kde.org/) to organize my music really nicely. It organized them by filetype, first letter of artist, artist, and album. The problem was, it left some dangling folders that I wanted to delete so my library looked clean on the filesystem. So I decided to use a little bit of linux command line fun to get the folders removed.

<!--more-->

I ended up using the command ‘find’ to achieve this. The first thing I did was run this command:

`find -depth -type d -empty -exec rmdir {} ;`

Basically what this does is starts in the current directory (-depth) and checks for directories (-type d) that are empty (-empty), and execute (-exec) the rmdir command on every directory it finds matching the criteria mentioned earlier.

This left me with the problem of some directories that still had some stuff in them. Here’s what I did to get rid of the stuff in them:

`find -depth -name "*.Extension Here" -execdir rm {} +`

This basically does the same thing except instead of looking for directories it looks recursively for the expression we entered, which is all files matching the filetype (\*.filetype here). the “-execrmdir” paramater executes the command in the current directory that the find command is working in. Then it basically just removes any file it finds matching that extension.

Hopefully this will be as helpful for you as it was in this scenario to me.

Later,  
Jon
