---
title: "HowTo: Mount Bin/Cue files in Linux"
date: 2006-05-30T07:04:28-04:00
slug: "howto_mount_bincue_files_in_linux"
url: /2006/05/30/howto_mount_bincue_files_in_linux/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-05"]
categories:
  - "debian"
  - "linux"
tags: []
aliases:
  - "/2006/05/30/howto_mount_bincue_files_in_linux/feed/"
---

Okay, so I I lied a little bit. I’m not sure how to mount a straight bin/cue file combination in Linux, but I do know that it’s really easy to convert them into an ISO file, and then mount the ISO in debian based linux.

`sudo apt-get install bchunk`

The syntax from bchunk is as follows:  
bchunk [-v] [-p] [-r] [-w] [-s]

So if i wanted to convert image,bin and image.cue into image.iso, I’d run the command:  
`bchunk image.bin image.cue image.iso`

Then to mount the ISO in linux you run the command:  
`mount -o loop -t iso9660 image.iso /mnt/image`, where image.iso is the iso is the image that you want to mount and /mnt/image is the mount directory.

Hopefully you’ll find a use for this like I did. If it doesnt work feel free to leave me an email at howe -dot- jon -at- gmail -dot- com and I’ll respond as quick as I can.

Later,  
Jon Howe
