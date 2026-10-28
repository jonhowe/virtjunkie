---
title: "uTorrent RSS"
date: 2006-04-20T10:12:14-04:00
slug: "utorrent_rss"
url: /2006/04/20/utorrent_rss/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-04"]
categories:
  - "general"
tags: []
aliases:
  - "/2006/04/20/utorrent_rss/feed/"
---

Adding a feed

Click on the RSS button, then click Add. Paste in the feed URL and hit OK. If you want to name the feed, simply type the name in front of the URL, like so:  
TV Feed|http://somesite.com/rss.xml (NO SPACE BEFORE OR AFTER THE | )

Note that the RSS Downloader will NOT consume any extra resources if you have no feeds present/enabled. Some feeds do not give direct links to the .torrent files (most notably Mininova) and as such won’t work, but you can use the MiniRSS feed fixer to modify those feeds to work properly. For Mininova’s feeds, you can use MiniRSS.org

Disabling a feed or filter

Simply uncheck the box next to the feed or filter, and it will no longer be used.

Renaming a feed or filter

You can rename a feed by selecting it, then single clicking or pressing F2. You can do the same thing for renaming filters.

Sorting filters

You can sort filters by drag and drop. Simply click, hold, and drag to wherever in the list you’d like it.

Using feeds that require HTTP authentication

For feeds that require HTTP authentication, simply use this format for the feed URL: http://username:password@sometorrentsite.com/rss.php

Using feeds that require cookies

To use feeds that require cookies, you must find the cookie for the site, and grab UID and pass from it.

\* IE users will find their cookies in %UserProfile%Cookies  
\* Firefox users will find their cookies in Tools -> Options -> Privacy -> Cookies -> View Cookies  
\* Opera users will find their cookies in Tools -> Advanced -> Cookies, but they must scroll down manually, find doesn’t work  
\* Users of other browsers will have to consult their browser’s documentation

Once you have the appropriate information, use this format for the feed URL:  
http://sometorrentsite.com/rss.php:COOKIE:…jh12378912y3lkj

Some sites do not use uid and pass as the variables, or use additional ones, so you MUST use the exact variable name and the extra variables they specify! For example, on a certain site, it uses id, password, and secure as the cookie variables you must use.

Automatically downloading torrents

To automatically download specific torrents from a feed, you can use Favorites to specify your own filters to grab torrents. It does NOT support regular expressions. Here’s a tutorial explaining the various options and how to use them (with examples).

\* Hit Add, then type the name of the filter.  
\* Click on the editbox next to Filter: and add your filter. The allowed wildcards are \* ? and |. An example of a filter you could use would be \*MP3 Archives\*  
If you have a strange feed using underscores or something besides periods, you can also try something like \*Go?Open\*  
You cannot specify the season or episode number in the filter if it is decoded by
