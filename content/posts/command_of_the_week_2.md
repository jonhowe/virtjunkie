---
title: "Command of the week #2"
date: 2005-09-19T21:01:14-04:00
slug: "command_of_the_week_2"
url: /2005/09/19/command_of_the_week_2/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-09"]
categories:
  - "general"
tags: []
aliases:
  - "/2005/09/19/command_of_the_week_2/feed/"
---

This week’s command is: *alias*

This command is great. In short it allows you to create [Pseudo](http://en.wikipedia.org/wiki/Pseudo) commands.

For example, on the server that this site runs on (my server), I regularly need to check to see what connections my computer has initiated, and what services they’re through. I do this using the linux command netstat using the following command line string: “`netstat -pan | grep tcp`“. Since I’m not doing this blog on netstat I will not explain that to you. If you have any questions, just comment on this post below and either me(Jon) or Kyle will attempt to explain it to you.

Now isn’t that command a little bit cumbersome? I think so at least. This is where alias comes in handy.

To set up an alias in your \*nix based profile do the following things:

1. Login as your user
2. Type in **`cd ~`**
3. Edit your `.bashrc` file using the text editor of your choice. I’ll be using vi, so I’ll type in **`vi .bashrc`**
4. You create an alias using the following syntax: alias NEW\_COMMAND=”COMMAND STRING\_TO BE EXECUTED”
5. Using the example above you would type in the following: alias ns=”netstat -pan | grep tcp”

So now anytime that you enter “ns”, “netstat -pan | grep tcp” will be executed in it’s place.

I should mention that you don’t have to place the alias command in your .bashrc file. You can also run it on the commnad line, but it will only have its effect for the current session.

Hopefully this’ll help you out at some point.

More later,  
Jon Howe
