---
title: "I’m Okay (and so is my blog)…."
date: 2006-07-27T22:13:02-04:00
slug: "im_okay_and_so_is_my_blog____"
url: /2006/07/27/im_okay_and_so_is_my_blog____/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-07"]
categories:
  - "linux"
  - "servers"
tags: []
aliases:
  - "/2006/07/27/im_okay_and_so_is_my_blog____/feed/"
---

Long story short:

The computer that this blog is on was up for over 220 days, and when I restarted it, things were all messed up.

The only thing that I really wanted to back up was this blog, but I was unable to dump the mysql database because I couldn’t get it (mysql) to start.

I ended up copying the raw database in /var/lib/mysql to a backup directory.

Then I went on this whole crazy journey trying to convert my drupal database to be used with wordpress…… That didn’t work too well.

Then I realized that all along all that I had to do is enable mod rewrite in apache in order for it to work.

So there you have it: how my blog is working, and why I sound a little bit scatterbrained.

More later (hopefully),  
Jon Howe
