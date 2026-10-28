---
title: "Howto: Kernel Building in Debian Sarge (3.1)"
date: 2006-01-25T03:36:37-05:00
slug: "howto_kernel_building_in_debian_sarge_3_1"
url: /2006/01/25/howto_kernel_building_in_debian_sarge_3_1/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-01"]
categories:
  - "debian"
  - "linux"
tags: []
aliases:
  - "/2006/01/25/howto_kernel_building_in_debian_sarge_3_1/feed/"
---

I’ve tried and tried to build my own custom kernel over the past year or so, usually only to stop in frustration because of some small part of the process not working.

This is all different now.

I found out that using the took make-kpkg makes things way easier. In fact I configured, compiled, and installed kernel 2.6.15 in about 30 minutes including the time that it took me to build it.

Here’s the process that I followed to achieve this:

1. Get required packages `apt-get install libncurses5-dev fakeroot bzip2 kernel-package`
2. Get latest kernel package from [Kernel.org](http://www.kernel.org/). The latest one at the time of this post is linux-2.6.15.tar.bz2.
3. Decompress the kernel archive (`tar -xjvf linux-2.6.15.tar.bz2`)
4. Start the kernel configuration tool (`make menuconfig`)

I should mention that it was way easier for me to load my existing kernel configuration, which was located at `/boot/config-(kernel version here)`.

5. make-kpkg clean
6. fakeroot make-kpkg –initrd –revision=myfirstkernelbuild\_v.0.1 kernel\_image

This runs make-kpkg as root, while making it so that initrd can load the kernekl. –revision is just the revision of the kernel, and kernel\_image is just the name of the kernel that you’re building.

The output of this command is kernel-image-2.6.15\_myfirstkernelbuild\_v.0.1.deb

7. Install the kernel (`dpkg -i kernel-image-2.6.15_myfirstkernelbuild_v.0.1.deb`)
8. Restart the computer (`init 6`)

If this process worked the output of `uname -r` should be 2.6.15.

Let me know if you have any problems.

Later,  
Jon Howe
