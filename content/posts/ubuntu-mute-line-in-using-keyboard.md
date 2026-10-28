---
title: "Ubuntu – Add Keyboard Shortcut for line in"
date: 2018-12-12T17:30:38-05:00
slug: "ubuntu-mute-line-in-using-keyboard"
url: /2018/12/12/ubuntu-mute-line-in-using-keyboard/
author:
  - "jhowe"
year: ["2018"]
month: ["2018-12"]
categories:
  - "uncategorized"
tags: []
aliases:
  - "/ubuntu---mute-line-in-using-keyboard/"
  - "/2018/12/12/ubuntu-mute-line-in-using-keyboard/feed/"
---

I use the line in connection on my desktop to route audio for sources other than my PC to the speaker system attached to my computer. For whatever reason, this is still annoyingly cumbersome, even in 2018. For years, I’ve done this by using Alsamixer, a command line mixer. This is fine enough, I guess, but I wanted something a bit more intuitive. The finished result shows the screen popup below, and is triggered by a key combination that executes a script.

<!--more-->

![](/wp-content/uploads/2018/12/image-1.png)

After

![](/wp-content/uploads/2018/12/image.png)

Before

To duplicate this on your system, you’ll need a [copy of the script from my github.](https://github.com/jonhowe/Virtjunkie.com/blob/master/toggleLineIn.sh) Once you have it, open Settings, Devices, and then select Keyboard:

![](/wp-content/uploads/2018/12/image-2.png)

Scroll all the way down to the bottom of the keyboard shortcuts, and select  the “+” to create a new shortcut.

![](/wp-content/uploads/2018/12/image-3.png)

As you can see, I’ve already got a couple of custom keyboard shortcuts there. I’ll show you how to create one to mute your line in input using the keyboard. Once you click the “+”, the screen below will appear. You’ll want to select your own keyboard shortcut, and ensure you’re using the correct path to the script.

![](/wp-content/uploads/2018/12/image-4.png)

Below is a copy of the script:

```text
#!/bin/bash
#/2018/12/12/ubuntu-mute-line-in-using-keyboard/
#https://github.com/jonhowe/Virtjunkie.com/blob/master/toggleLineIn.sh

OUT=$(amixer sset Line toggle)
RESULT=$(echo $OUT | grep "Left:" | cut -d'[' -f4 | cut -d ']' -f 1)
#notify-send pulls icons from /usr/share/icons/gnome/32x32
notify-send "Toggling Line In" "Line in is now: $RESULT" -i audio-volume-low
```

Note 1:

In order for this to work, you may need to ensure that Loopback is enabled. The easiest way to do this is to install the alsa-utils package, and run Alsamixer to enable it.

![](/wp-content/uploads/2018/12/image-5.png)
