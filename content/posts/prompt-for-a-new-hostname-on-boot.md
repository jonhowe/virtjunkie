---
title: "Prompt For A New Hostname on Boot"
date: 2018-11-25T21:52:25-05:00
slug: "prompt-for-a-new-hostname-on-boot"
url: /2018/11/25/prompt-for-a-new-hostname-on-boot/
author:
  - "jhowe"
year: ["2018"]
month: ["2018-11"]
categories:
  - "automation"
  - "linux"
  - "scripting"
tags:
  - "bash"
  - "linux"
  - "scripting"
  - "ubuntu"
aliases:
  - "/prompt-for-a-new-hostname-on-boot/"
  - "/2018/11/25/prompt-for-a-new-hostname-on-boot/feed/"
---

I’ve been brushing up on a few technologies in my home lab, and have found myself using VMware workstation for some simple tasks that don’t require a whole virtualized environment. Workstation didn’t set the hostname of my Ubuntu 18.xx VMs properly after they booted. Maybe I’m a little spoiled by guest OS customization or missing something, but either way, I needed a way to quickly spin up a whole VM and have it’s hostname set correctly. It’s definitely not the cleanest, and I realize I would be better off using the Workstation Pro REST API, but I’m not there yet.

<!--more-->

We can do this pretty easily by adding a script to the /etc/profile.d directory. The script I’m currently using is below:

```bash
#!/bin/bash
#file /etc/profile.d/VirtJunkie.com-set_hostname.sh
FLAG="/var/log/firstboot.flag"
if [ ! -f $FLAG ]; then
    echo "Server will reboot after this process completes"
    echo -n "Current hostname is $(hostname). Enter the new hostname and press [ENTER]: "
    read newhostname
    sudo hostnamectl set-hostname $newhostname

    #the next line creates an empty file so it won't run the next boot
    sudo touch $FLAG
    sudo reboot now
fi
```

Just modify your parent image, clone your test VMs, and this will prompt you to set a new hostname the first time you log in.
