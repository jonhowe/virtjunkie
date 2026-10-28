---
title: "Disable Multiple Services using Powershell"
date: 2013-04-21T17:00:53-04:00
slug: "disable-multiple-services-using-powershell"
url: /2013/04/21/disable-multiple-services-using-powershell/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-04"]
categories:
  - "uncategorized"
tags: []
aliases:
  - "/2013/04/21/disable-multiple-services-using-powershell/feed/"
---

Over the past few months I’ve been doing a lot of work that’s required me to get into the Services control panel on Windows Server.  While it’s fairly easy to get in and change the status of one service using the windows services control panel (WIN+R, Services.msc), it gets annoying when you need to do this multiple times, and even worse if you need to take action on multiple services.

Fortunately, powershell gives us the ability to do this very easily.

Here’s how:

<!--more-->

The command below is the building block for everything else you want to do with a service. Since vendors don’t provide a standard prefix with their service names (ahem, vmware – or in this case, HP), you need to use the -DisplayName parameter of this commandlet. You can use the asterisk as a wildcard.

```powershell
Get-Service -DisplayName "HP*
```

![get-service -displayname](/wp-content/uploads/2013/04/get-services-300x109.png)

Once you have a set of services, you can pipe them to another commandlet, and take action, such as stopping the service, or disabling automatic startup.

Run this command to stop the services.

```powershell
Get-Service -DisplayName "HP* | Stop-Service
```

Run the command below in order to disable these services from starting automatically

```powershell
Get-Service -DisplayName "HP* | Set-Service -StartupType "Disabled"
```
