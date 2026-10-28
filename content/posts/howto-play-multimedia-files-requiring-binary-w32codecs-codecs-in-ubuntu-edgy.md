---
title: "Howto: Play Multimedia Files Requiring Binary (w32codecs) Codecs in Ubuntu Edgy"
date: 2006-11-15T10:06:06-05:00
slug: "howto-play-multimedia-files-requiring-binary-w32codecs-codecs-in-ubuntu-edgy"
url: /2006/11/15/howto-play-multimedia-files-requiring-binary-w32codecs-codecs-in-ubuntu-edgy/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-11"]
categories:
  - "linux"
tags: []
aliases:
  - "/2006/11/15/howto-play-multimedia-files-requiring-binary-w32codecs-codecs-in-ubuntu-edgy/feed/"
---

I’ve been trying to do this for a while, and finally this morning I came to a solution.

To do this follow the following steps:

<!--more-->

1. Add the following line to your /etc/apt/sources.list with the following command: **sudo wget http://medibuntu.sos-sts.com/sources.list.d/edgy.list -O /etc/apt/sources.list.d/medibuntu.list**
2. Run the following command: **wget -q http://medibuntu.sos-sts.com/repo/medibuntu-key.gpg -O- | sudo apt-key add –**
3. Run the following command: **sudo apt-get update**
4. Run the following command: **sudo apt-get install w32codecs**

Now enjoy playing all of your media files that require proprietary codecs.
