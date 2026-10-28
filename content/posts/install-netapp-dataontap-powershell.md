---
title: "Install NetApp DataOnTap Powershell"
date: 2013-02-10T12:27:40-05:00
slug: "install-netapp-dataontap-powershell"
url: /2013/02/10/install-netapp-dataontap-powershell/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-02"]
categories:
  - "netapp"
  - "powershell"
  - "scripting"
  - "automation"
  - "servers"
tags: []
aliases:
  - "/2013/02/10/install-netapp-dataontap-powershell/feed/"
---

I have been using the NetApp Data ONTAP toolkit a lot lately, and I’m going to throw some tutorials on this site relating to it.

Let’s go through the steps we need to follow to get the toolkit installed on your machine.

<!--more-->

1. [Download the NetApp Data ONTAP Toolkit](https://communities.netapp.com/docs/DOC-22259 "Download the NetApp Data ONTAP Toolkit") – You will need a NetApp Now account to download it
2. Install the MSI
3. Open Powershell
4. Load the Data ONTAP module:
   1. Import Module dataontap
5. Learn about what you can do
   1. show-nahelp
