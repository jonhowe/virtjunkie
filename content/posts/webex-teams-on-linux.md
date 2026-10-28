---
title: "Webex Teams on Linux"
date: 2019-06-01T09:59:50-04:00
slug: "webex-teams-on-linux"
url: /2019/06/01/webex-teams-on-linux/
author:
  - "jhowe"
year: ["2019"]
month: ["2019-06"]
categories:
  - "electron"
  - "linux"
  - "ubuntu"
tags: []
aliases:
  - "/2019/06/01/webex-teams-on-linux/feed/"
---

![](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Electron_Software_Framework_Logo.svg/1200px-Electron_Software_Framework_Logo.svg.png)

My company standardized on [Cisco Webex Teams](https://teams.webex.com/) for persistent chat. Unfortunately, webex teams does not have a linux client, and recommends that people simply use the web client. Unfortunately, I’m more used to this answer than I’d like, but fortunately I don’t have to any more.

<!--more-->

This morning I found a project called [Nativefier](https://github.com/jiahaog/nativefier). It allows you to make any web page a desktop application using electron and a handful of other tools.

Their github page has documentation on how to do the install, but i’ll also add my exact steps. Keep in mind, I’m using Ubuntu 19.04 so YMMV.

You’ll need to have npm installed, and use it to install nativefier.

1. sudo apt install npm
2. sudo npm install nativefier -g

I manually went to the internet to grab an icon for webex teams that I had the packager use. Feel free to download it and use it, however, from what I read in the documentation, nativefier should have the ability to find the icon automatically. I didn’t try it, but if you do, let me know how it works!

[cisco-webex-teams](/wp-content/uploads/2019/06/cisco-webex-teams.png)[Download](/wp-content/uploads/2019/06/cisco-webex-teams.png)

You can use the following snippet to convert convert webex teams into an application.

```text
nativefier -n "Webex-Teams" -p linux -a x64 -e 4.2.3 -i [absolute-path-to]/cisco-webex-teams.png --tray https://teams.webex.com
```

That will create a directory called “webex-teams-linux-x64”. To open webex teams, enter that directory and run the webex-teams binary.
