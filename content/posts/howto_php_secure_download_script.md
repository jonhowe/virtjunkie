---
title: "Howto: PHP Secure Download Script"
date: 2006-03-25T08:10:14-05:00
slug: "howto_php_secure_download_script"
url: /2006/03/25/howto_php_secure_download_script/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-03"]
categories:
  - "php"
  - "web-development"
tags: []
aliases:
  - "/2006/03/25/howto_php_secure_download_script/feed/"
---

I’ve been wanting to make a script in PHP that handles downloads for a while. Last night I was bored, so I made one.

DISCLAIMER:  
This is a very basic example, but if you have any use for this, I’m sure that you can figure out how to use it. If not, I’ll probably work more with it in the future anyways.

This system works with two PHP files.

If you just want to see the script work, go [Here](/blog/blogfiles/dlkeeper/dl.php).

From there you can download a sample file and see the source of the scripts.

Now, for how it works…

All that the first script (dl.php) does is display a link to the main download script (which handles the actual download) and sets a session variable for 60 seconds in the future.

Once you click on the link, the main download script (dl2.php) sets another session variable containing the time that the link was clicked.

It checks to see if the time that dl.php was generated no more than 60 seconds later than the link was clicked. If it was later than that the download fails.

Feel free to email me (howe -dot- jon -at- gmail -dot- com) if you have any questions, or requests or whatever, and I’ll do my best to get back to you that day.

Later,  
Jon Howe
