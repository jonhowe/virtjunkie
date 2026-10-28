---
title: "Howto: Get a Movie from a DVD to your Sony Clie (and probably other PDA’s as well)"
date: 2006-03-08T07:56:10-05:00
slug: "howto_get_a_movie_from_a_dvd_to_your_sony_clie_and_probably_other_pdas_as_well"
url: /2006/03/08/howto_get_a_movie_from_a_dvd_to_your_sony_clie_and_probably_other_pdas_as_well/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-03"]
categories:
  - "debian"
  - "linux"
tags: []
aliases:
  - "/2006/03/08/howto_get_a_movie_from_a_dvd_to_your_sony_clie_and_probably_other_pdas_as_well/feed/"
---

I’ll try to make this as simple as possible.

I’m going to assume that you’re using Linux (and that you are not a complete noob at it) for this tutorial. I will assume that you’re using a Sony Clie.

Here’s an overview of what we’re going to do:

1. Rip dvd using DVD:Rip
2. Convert ripped movie into a clie compatible format
3. Download and install TCPMP (free media player)
4. (optional) Install Memory Stick Pro fix
5. Copy Movie to the Memory Stick

**Step 1: Download and Install Files**  
*apt-get install dvdrip*  
*apt-get install pilot-link*  
*[Download TCMP (for palm)](http://tcpmp.corecodec.org/download)*  
*Download all attachments*

**Step 2: Rip DVD**  
*Encode with the xvid4 codec*  
*Set file size to One CD at 700Mb*  
*The only reason that I have this step is because I like to watch the video in high quality on my desktop*

**Step 3: Convert ripped DVD to Palm Readable Format**  
*Put the following into a script called vid2palm and make it executable*

`#!/bin/sh  
#Change 480:320 to the size of your PDA screen  
#480:320 works for the Sony Clie`

nice mencoder $1 -vf scale=480:320 -ovc xvid -xvidencopts bitrate=300 -oac mp3lame -lameopts cbr:br=64 -o $2  
So, if dvdrip created the file MyMovie.avi you’d run the command *vid2palm MyMovie.avi MyMovie\_Palm\_Format.avi*

**Step 4: Install files on your Clie**  
This can be a little tricky for someone doing it for the first time, but after a couple of times it works great.

The syntax for installing a palm file is:  
*pilot-xfer /dev/pilot -i [File to be installed]*

However, If you just run this command it won’t work. You first need to hit the hotsync button and then quickly run the previous command.

If you do this and the console says to press the hotsync button, just hit cancel on your clie, and terminate the command, and try again. It’s been a bit of hit-and-miss for me.

Files to install on the PDA from the TCPMP Archive:

- pilot-xfer /dev/pilot -i tcpmp\_ffmpeg\_plugin.prc
- pilot-xfer /dev/pilot -i tcpmp\_mp3\_plugin.prc
- pilot-xfer /dev/pilot -i tcpmp\_mpeg4\_plugin.prc
- pilot-xfer /dev/pilot -i tcpmp.prc
- As well as the attached tcpmp\_aac\_plugin.prc

If your memory card is a memory stick **pro** it will not work by default with the clie, so you have to install a fix for it (it’s the MSPRONX\_ENUS.PRC one):  
*pilot-xfer /dev/pilot -i MSPRONX\_ENUS.PRC*

Sound doesn’t work by default on mine either, I had to install the following patch (again, an attachment: MCA2\_05\_TEST.prc):  
*pilot-xfer /dev/pilot -i MCA2\_05\_TEST.prc*

You need to set up this plugin by going to prefrences and then in the drop down menu select MCA2, and check the button “auto install after reset”. It will restart, then go back to the same area and select “DEFAULT is ON (normal)”.

**Step 5: Moving the finished product to your Memory Stick (pro)**  
First, goto MS Import. If you have a newer distro / kde it will mount the flash drive as a local directory. If it doesnt, use the “mount” command to mount it. I assume that you know how to do this (if you don’t try “man mount”).

Now it’s a bit of a waiting game. Once it looks like it’s done copying unmount the device in linux first, wait a minute, and then disconnect in MS Import.

**Step 6: Play the Movie**  
Goto TCPMP, open, and play your movie!

This is how I did it, after a week or so of trying.

If you have any questions leave a comment or email me (howe -dot- jon -at- gmail -dot- com.

Later,  
Jon Howe
