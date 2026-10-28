---
title: "AJAX Based MySql Live Search"
date: 2006-04-03T18:02:25-04:00
slug: "ajax_based_mysql_live_search"
url: /2006/04/03/ajax_based_mysql_live_search/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-04"]
categories:
  - "mysql"
  - "php"
  - "web-development"
tags: []
aliases:
  - "/2006/04/03/ajax_based_mysql_live_search/feed/"
---

This is a little something that I made up this afternoon at school.

It’s an implementation of a search app with out a celing. In other words , there’s no submit button. With each keystoke that you type, the query get’s more accurate.

If you just want to check it out (with source, and an example) then [Click Here](/blog/blogfiles/ajax_db_search/ajaxSearch.php)  
The code is commented pretty well.

If you want a little explanation read on.

I used a library called [Xajax](http://www.xajaxproject.org/) for this project (and the last one as well). It’s an extremely useful and easy to use library because of the fact that it doesn’t require the coder to know any javascript. This is a goood thing, because I HATe javascript.

The Xajax library allows you to take a PHP function and essentially use it as a javascript function asynchronously.

What this script does is check to see if the user presses a key. Each time that they do the PHP function autoSearch() runs. autoSearch() has one paramater, the current value of the input box. Read the code comments for more info on this.

If the entered query is 2 or more charachters, then a mysql query is executed. If there are result(s), then they are diplayed.

Practical Application:  
Personally, I hope to use this in the content mananagement system that I’ll be starting soon. I’m planning on having it parse through blog entries, and display the title and the publishing date of the post.

When you click on the link above you’ll see the example page. At the bottom of it are links to the PHP source, as well as the MySql Source.

If you have any questions email me at “howe -dot- jon – at – gmail – dot – com”, and I’ll get back as soon as I can.

Later,  
Jon Howe
