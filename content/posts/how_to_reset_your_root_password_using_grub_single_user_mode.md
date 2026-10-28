---
title: "How To Reset Your Root Password Using Grub Single User Mode"
date: 2006-07-28T16:03:21-04:00
slug: "how_to_reset_your_root_password_using_grub_single_user_mode"
url: /2006/07/28/how_to_reset_your_root_password_using_grub_single_user_mode/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-07"]
categories:
  - "linux"
tags: []
aliases:
  - "/2006/07/28/how_to_reset_your_root_password_using_grub_single_user_mode/feed/"
---

Today I was confronted by someone who lost their root password, lucky for them they were using grub as their bootloader and it wasn’t password protected. **This is the default for Ubuntu, Fedora, and other distros**

There are X steps to this process:

**Step 1. Get into the Grub Editor**  
When you boot you’ll probably see a few options in your grub menu. Unless you’re sure what kernel that you want to use, select the kernel at the top of the list and **press e**.

**Step 1.1 Get into the Grub Editor (Part 2)**  
Hit the down arrow until the line that starts with **kernel** is selected, then **press e again**

**Step 2. Enable Single User Mode**  
All that you have to do in order to enable single user mode is  **add the word “single”** to the end of the line. Hit enter to return to the previous screen.

**Step 3. Boot into your Single User Environment**  
With the same kernel selected **press b** to boot into the your new os.

Now you should be in a nice shiny root prompt. Feel free to do whatever you want here, including **typing passwd** to change the root passwd.
