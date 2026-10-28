---
title: "Problems with AllPeers in Firefox"
date: 2007-03-12T23:26:22-04:00
slug: "problems-with-allpeers-in-firefox"
url: /2007/03/12/problems-with-allpeers-in-firefox/
author:
  - "jhowe"
year: ["2007"]
month: ["2007-03"]
categories:
  - "firefox"
tags: []
aliases:
  - "/2007/03/12/problems-with-allpeers-in-firefox/feed/"
---

I found out recently, like a lot of people, that the [AllPeers](http://www.allpeers.com/ "AllPeers") Firefox extension went Open Source. So naturally, I realized the hype it created and installed it.

Unfortunately, I never tested it, because none of my friends wanted to install it, so there it sat right there in my Firefox installation, dormant. It wasn’t until today that I had problems with it.

I restarted my computer today, and tried to start up Firefox, and it did nothing… So I started up the console, and started Firefox. It started starting up fine, with loading of AllPeers, then had a segmentation fault error…

I ended up having to remove the extension finally. To do this use the following steps:

1. Open up your terminal emulator
2. Navigate to ~/.mozilla/firefox
3. There should be a directory there that has a bunch of seemingly random characters. Mine’s tr1d6tmr.default. Navigate to that directory.
4. Navigate to the extensions directory.
5. Execute ‘find ./ | grep peers’ and delete the directory things were found in.

Now if you were having the same problems as me, you should be able to start Firefox again!

Jon Howe
