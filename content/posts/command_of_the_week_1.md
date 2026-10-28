---
title: "Command of the week #1"
date: 2005-09-12T20:55:32-04:00
slug: "command_of_the_week_1"
url: /2005/09/12/command_of_the_week_1/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-09"]
categories:
  - "general"
tags: []
aliases:
  - "/2005/09/12/command_of_the_week_1/feed/"
---

This week’s command is: *screen*

I actually just found this command recently. It’s a great little treasure that expands the use of unix in a huge way. Let me explain.

For those of you who don’t know, Unix uses a CLI (or Command Line Interface), meaning that there are no “windows” or “X” boxes to close the windows, it’s all handeled by the keyboard and text on the screen.

Multitasking is critical with computers, and until recently, I’ve been cheating by opening up separate windows in my SSH (or Secure Shell) client. This can be a little bit tiring because you have to connect to the server each time you make a new window.

Screen takes care of this completely by allowing you to have multiple of what I like to call “virtual sessions”. Now an example.

So you connect to your server and want to have one of these so-called “virtual sessions”. It’s easy. Just get to the command line and enter `screen`.

Your screen should go blank, Congrats! Your in a virtual session.

In order for you to go back to your original session hit ctrl + a and then d.

This closes your virtual session, but keeps it open in memory. If you want to close it completely, just hit ctrl + a and then hit shift + d, or uppercase D.

Either of these two will bring you back to your original screen and will either keep the contents intact or destroy them.

Now that you’re back at your original screen just hit screen -s to restore your session! It’s as easy as that.

Maybe I’ll add some more advanced features of screen later this week, and give ya a freebie.

More later,  
Jon Howe
