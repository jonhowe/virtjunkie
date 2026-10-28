---
title: "Problems when running apt-get on Debian"
date: 2005-12-06T22:27:57-05:00
slug: "problems_when_running_apt-get_on_debian"
url: /2005/12/06/problems_when_running_apt-get_on_debian/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-12"]
categories:
  - "debian"
tags: []
aliases:
  - "/2005/12/06/problems_when_running_apt-get_on_debian/feed/"
---

I’ve been having some problems using apt-get lately which led me to doing an apt-get dist-upgrade.

Smart me found this command on the internet and decided to use it. It worked just fine, except for the fact that when I restarted my computer the graphical display manager that I use didn’t start.

Here’s the steps that I took to diagnose the problem.

1. I tried to start gdm instead of kdm by editing`'/etc/X11/default-display-manager'`. This file contains the path to your display manager, for me it was `'/usr/bin/kdm'`
2. I tried changing that to `'/usr/bin/gdm'` and I received an X server error saying that my chosen X server (XFree86) was not found.I thought that this was a little funny because I didn’t think that I used XFree86, but Xorg instead.
3. So, I looked at the file `'/etc/X11/X'`, which is a symbolic link (which is like a shortcut in windows) and found out that in the upgrade it changed the link to point to a nonexistent file.
4. After that I changed the link to point to `'/usr/bin/X11/Xorg'` and voila, kdm started up just fine.More Later,  
   Jon Howe
